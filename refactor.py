import threading
import time
import random

waitQueue = [[], [], []]    # Fila de espera
counterGender = [0,0,0]    # Contador para cada gênero
counterWaitTime = [0,0,0]   # Contador para o tempo de espera de cada gênero
bathroom = None
persons = 0

# Variável de sincronização
mutexGender = threading.Semaphore()  # Mutex para acesso a variável genderBathroom

class Person(threading.Thread):
    def __init__(self, personId):
        threading.Thread.__init__(self)
        self.personId = personId
        self.gender = self.generateGender()
        self.waitTime = 0

    def generateGender(self):
        random.seed()
        gender = random.randint(0,2)
        while(counterGender[gender] >= persons/3):
            gender = random.randint(0,2)
        counterGender[gender] += 1
        return gender
    
    def enterBathroom(self):
        global bathroom, waitQueue, mutexGender

        if bathroom.genderBathroom == -1:
            mutexGender.acquire()
            bathroom.genderBathroom = self.gender
            mutexGender.release()
            print("🚻 Banheiro Livre. Gênero no banheiro: {}.".format(bathroom.genderBathroom))

        if bathroom.genderBathroom != self.gender:
            waitQueue[self.gender].append(self)
            
            print("FILA ⌛: Pessoa {} - Gênero: {} entrou na fila.".format(self.personId, self.gender))

            print("Fila Gênero {}: [".format(self.gender),end="")
            for i in range(len(waitQueue[self.gender])):
                print("{} ".format(waitQueue[self.gender][i].personId), end="")
            print("]")
                
        if bathroom.boxes == 0:
            if self not in waitQueue[self.gender]:
                waitQueue[self.gender].append(self)
                print("FILA ⌛: Pessoa {} - Gênero: {} entrou na fila.".format(self.personId, self.gender))

                print("Fila Gênero {}: [".format(self.gender),end="")
                for i in range(len(waitQueue[self.gender])):
                    print("{} ".format(waitQueue[self.gender][i].personId), end="")
                print("]")
        
        with bathroom.semaphore:
            self.getStall() 

    def getStall(self):
        global bathroom, waitQueue, counterWaitTime
        
        counterWaitTime[self.gender] += time.time() - self.waitTime

        try:
            waitQueue[self.gender].remove(self)
        except(ValueError):
            pass

        bathroom.boxes -= 1 
        
        print("ENTRADA 🚽: Pessoa {} - Gênero {} entrando no box. --- {} boxes livres.".format(self.personId, self.gender, bathroom.boxes))
        
        if len(waitQueue[self.gender]) > 0:
            print("Fila Gênero {}: [".format(self.gender),end="")
            for i in range(len(waitQueue[self.gender])):
                print("{} ".format(waitQueue[self.gender][i].personId), end="")
            print("]")
        
        time.sleep(5)
        if bathroom.boxes == (bathroom.maxBoxes - 1):
            bathroom.ocupationTime += 5

        bathroom.boxes += 1
       
        self.releaseStall()

    def releaseStall(self):
        global bathroom, waitQueue, mutexGender
        
        print("SAÍDA 🏃: Pessoa {} - Gênero {} saindo do box. {} boxes livres.".format(self.personId, self.gender, bathroom.boxes))

        # Se não houver pessoas do mesmo gênero na fila ocorrerá uma troca de gênero
        if bathroom.boxes == bathroom.maxBoxes:
            mutexGender.acquire()
            bathroom.genderBathroom = self.genderChange()
            print("Troca de gênero. Novo gênero: {}.".format(bathroom.genderBathroom, bathroom.genderBathroom - 1, bathroom.genderBathroom - 2))
            mutexGender.release()
    
    def genderChange(self): 
        global waitQueue
        
        if len(waitQueue[0]) == 0 and len(waitQueue[1]) == 0 and len(waitQueue[2]) == 0:
            return -1

        if len(waitQueue[0]) == 0: 
            if len(waitQueue[1]) > 0 and len(waitQueue[2]) > 0:
                if waitQueue[1][0].waitTime < waitQueue[2][0].waitTime:
                    return 1
                else:
                    return 2

            if len(waitQueue[1]) > 0 and len(waitQueue[2]) == 0:
                return 1
            else: 
                return 2

        if len(waitQueue[1]) == 0: 
            if len(waitQueue[0]) > 0 and len(waitQueue[2]) > 0:
                if waitQueue[0][0].waitTime < waitQueue[2][0].waitTime:
                    return 0
                else:
                    return 2

            if len(waitQueue[0]) > 0 and len(waitQueue[2]) == 0:
                return 0
            else: 
                return 2

        if len(waitQueue[2]) == 0: 
            if len(waitQueue[0]) > 0 and len(waitQueue[1]) > 0:
                if waitQueue[0][0].waitTime < waitQueue[1][0].waitTime:
                    return 0
                else:
                    return 1

            if len(waitQueue[0]) > 0 and len(waitQueue[1]) == 0:
                return 0
            else: 
                return 1

        if len(waitQueue[0]) > 0 and len(waitQueue[1]) > 0 and len(waitQueue[2]) > 0:

            times = []

            times.append(waitQueue[0][0].waitTime)
            times.append(waitQueue[1][0].waitTime)
            times.append(waitQueue[2][0].waitTime)

            return times.index(min(times))

    def run(self):
        print("CHEGADA 🧍: Pessoa{} - Gênero {} chegou no banheiro.".format(self.personId, self.gender))
        self.waitTime = time.time()
        self.enterBathroom()

class Bathroom(threading.Thread):
    def __init__(self, boxes):
        threading.Thread.__init__(self)
        self.boxes = boxes
        self.maxBoxes = boxes
        self.ocupationTime = 0
        self.semaphore = threading.Semaphore(boxes)
        self.genderBathroom = -1
        self.runtime = 0

    def run(self):
        global persons
        
        self.runtime = time.time()
        
        personId = 1
        threadList = []

        print("{} boxes e {} Pessoas".format(self.boxes, persons))

        for i in range(persons):
            random.seed()
            sleepTime = random.randint(2,6)

            thread = Person(personId)
            threadList.append(thread)

            thread.start()
            time.sleep(sleepTime)
            personId += 1
            
        for thread in threadList:
            thread.join()

        self.runtime = time.time() - self.runtime

def init():
    global bathroom, persons
    boxes = 0

    print("#######################")
    print("1 - 1 box e 60 pessoas")
    print("2 - 3 boxes e 180 pessoas")
    print("3 - 5 boxes e 300 pessoas")
    op = int(input("opção: "))
    print("#######################")
    while (op != 1 and op != 2 and op != 3):
       print("Invalido!")
       op = input("opção: ")
    
    if op == 1:
        boxes = 1
        persons = 60
    elif op == 2:
        boxes = 3
        persons = 180 
    elif op == 3: 
        boxes = 5 
        persons = 300

    bathroom = Bathroom(boxes)
    bathroom.start()
    bathroom.join()

    print("\n\n")
        
def main():
    global bathroom, counterWaitTime, persons

    init()
    
    print("\n\n############")
    print("Tempo de execução: {}min {:.2f}s".format(int(bathroom.runtime/60),bathroom.runtime%60))

    for i in range(3):
        print("Pessoas do Gênero {}: {}. Tempo médio de espera: {}min{:.2f}s".format(i,counterGender[i],int((counterWaitTime[i]/counterGender[i])/60), (counterWaitTime[i]/counterGender[i])%60))

    print("Taxa de Ocupação: {:.2f}%.".format(bathroom.ocupationTime*100/bathroom.runtime))

if __name__ == "__main__":
    main()
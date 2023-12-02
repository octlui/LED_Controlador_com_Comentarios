import cv2 #biblioteca cv2 que pega o vídeo da webcam
import mediapipe as mp #biblioteca mediapipe que reconhece a imagem e é capaz de detectar a mão
import time
import controller as cnt
time.sleep(2.0) #tempo de resposta de 2s

mp_draw=mp.solutions.drawing_utils  #pega os circulos
mp_hand=mp.solutions.hands      #pega a mão inteira 

tipIds = [4,8,12,16,20] #são os pontos onde terminam cada um dos dedos

video=cv2.VideoCapture(0) #captura usando a câmera do computador por padrão(número 0)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands: #parâmetros para a biblioteca mp no que diz respeito às mãos(padrão)

    while True:
        ret,image = video.read() #retorna um valor int 0 ou 1 na var ret cada vez que captura um frame (assim, testa a funcionalidade)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #coloca a imagem em cor especifica
        image.flags.writeable = False #torna a imagem apenas leitura
        results = hands.process(image) #processando a imagem para ser usada no mp
        image.flags.writeable = True #torna a imagem passível de edit
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #passa para RGB
        lmList = [] #cria lista vazia
        if results.multi_hand_landmarks: #detecta alguma mão na imagem
            for hand_landmark in results.multi_hand_landmarks: #para cada mão detectada
                myHands= results.multi_hand_landmarks[0] #var myHands guarda os landmarks da mão detectada
                for id, lm in enumerate(myHands.landmark): #pega os ids de cada círculo
                    h,w,c = image.shape #obtem dimensões
                    cx,cy = int(lm.x*w), int(lm.y*h) #obtem coordenadas
                    lmList.append([id,cx,cy]) #coloca para cada id suas respectivas coordenadas

                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS) #conecta os circulos à mão, através do processamento da imagem

        fingers = [] #cria lista vazia para armazenar os dedos

        if len(lmList) != 0: #se a lista lmList não está vazia:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]: #comparação das coordenadas de um dedo em comparação a outro (se a coordenada da ponta for maior que a outra, o dedo estará estendido)
                fingers.append(1)   #dedo estendido - adiciona à lista dedos
            else:
                 fingers.append(0)  #dedo dobrado
            for id in range(1,5): 
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)
            cnt.led(total) # passa para o arquivo controller o número total
            if total == 0:
                cv2.rectangle(image,(20,300), (270,425), (0,255,0), cv2.FILLED)
                cv2.putText(image, "0", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
                cv2.putText(image, "LED", (100,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
            elif total == 1:
                cv2.rectangle(image,(20,300), (270,425), (0,255,0), cv2.FILLED)
                cv2.putText(image, "1", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
                cv2.putText(image, "LED", (100,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
            elif total == 2:
                cv2.rectangle(image,(20,300), (270,425), (0,255,0), cv2.FILLED)
                cv2.putText(image, "2", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
                cv2.putText(image, "LEDs", (100,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
            elif total == 3:
                cv2.rectangle(image,(20,300), (270,425), (0,255,0), cv2.FILLED)
                cv2.putText(image, "3", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
                cv2.putText(image, "LEDs", (100,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
            elif total == 4:
                cv2.rectangle(image,(20,300), (270,425), (0,255,0), cv2.FILLED)
                cv2.putText(image, "4", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
                cv2.putText(image, "LEDs", (100,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
            elif total == 5:
                cv2.rectangle(image,(20,300), (270,425), (0,255,0), cv2.FILLED)
                cv2.putText(image, "5", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
                cv2.putText(image, "LEDs", (100,375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5)
        
        #encerramento padrão        
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()


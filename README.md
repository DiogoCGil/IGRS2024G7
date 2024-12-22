## IGRS2024G7
#Membros do Grupo 07:

Diogo Gil-> 121763

Tomás Catarino -> 99227

-Ferramentas usadas :
  Wireshark 
  Twinkle 
  SEMS e SIP protocols
  Python
  
-Outras Informações :
  Para teste usamos a utilizadora Trudy no porto 4444, o utilizador Bob no porto 5555 e a utilizadora Alice no porto 6666
  O porto do servidor SIP é o 5060
  O porto do servidor de Anuncios SEMS é o 5080
  O porto do servidor de Conferencias SEMS é no 5090
  O serviço está todo no 127.0.0.1
  
  Foi implementado o Registro e as suas devidas respostas SIP para todos os casos
  Foi implementado as Chamadas e as suas devias respostas SIP para todos os casos
  Foi implementado o serviço de Anuncios busyann e inconference, para isto foir criado um metodo de verificação se o utilizador chamada está em uma chamada com outro utilizador ou está numa conferencia 
  Foi implementado o serviço de Conferencia 
  Foi implementado o serviço de Mensagens onde é verificado se enviado uma mensagem para o URI especial sip:validar@acme.pt com um PIN especifico é valido ou não em termos de segurança 
  
-Pontos incompletos :
  Foi implementado a verficação da introdução do digito 0 quando o utilizador está no sistema de anuncios inconference e se quer juntar tambem a essa conferencia , mas dá erro 481 e não se consegue juntar

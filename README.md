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
  Para testes, foram utilizados os seguintes utilizadores e portas:
    Trudy no porto 4444
    Bob no porto 5555
    Alice no porto 6666
  O servidor SIP está no porto 5060.
  O servidor de anúncios SEMS está no porto 5080.
  O servidor de conferências SEMS está no porto 5090.
  Todo o serviço é executado no endereço 127.0.0.1.
  
-Funcionalidades Implementadas:
  1.Registo e Respostas SIP:
    -Foram implementados todos os casos de registo, incluindo as respostas adequadas para cada cenário.
    
  2.Chamadas e Respostas SIP
    -Implementação completa das chamadas entre utilizadores, com as respetivas mensagens SIP.
  
  3.Serviço de Anúncios (busyann e inconference)
    -Foi criado um método para verificar se o utilizador chamado está:
        Já numa chamada com outro utilizador, ou
        Participar numa conferência.
  
  4.Serviço de Conferência
    -Implementação de conferências SIP.
  
  5.Serviço de Mensagens
    -Foi desenvolvido um sistema para validar mensagens enviadas para o URI especial sip:validar@acme.pt com um PIN específico, garantindo a segurança. 

  
-Pontos Incompletos
  Erro na Conferência:
    Foi implementada a verificação para introduzir o dígito "0" quando o utilizador está no sistema de anúncios inconference e deseja juntar-se à conferência.
    No entanto, ocorre um erro 481, e o utilizador não consegue entrar na conferência.

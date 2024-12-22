# IGRS2024G7
## Membros do Grupo 07:

Diogo Gil-> 121763

Tomás Catarino -> 99227



## Ferramentas Utilizadas  

- **Wireshark**, **Twinkle**, **SEMS** e protocolos **SIP**  
- **Python** para desenvolvimento  

## Outras Informações  

- **Utilizadores e Portas**:
  - **Trudy**: porto **4444**  
  - **Bob**: porto **5555**  
  - **Alice**: porto **6666**  
- **Servidores e Portas**:
  - **Servidor SIP**: porto **5060**  
  - **Servidor de Anúncios SEMS**: porto **5080**  
  - **Servidor de Conferências SEMS**: porto **5090**  
- Todos os serviços estão configurados no endereço **127.0.0.1**.  

## Funcionalidades Implementadas  

1. **Registo e Respostas SIP**  
   - Implementação de todos os casos de registo, com as respostas adequadas.  

2. **Chamadas e Respostas SIP**  
   - Chamadas entre utilizadores com suporte completo para mensagens SIP.  

3. **Serviço de Anúncios**  
   - Implementados os anúncios **busyann** e **inconference**, com verificação do estado do utilizador:
     - Se está numa chamada com outro utilizador, ou  
     - Se está numa conferência.  

4. **Serviço de Conferência**  
   - Implementação completa para criação e gestão de conferências SIP.  

5. **Serviço de Mensagens**  
   - Sistema de validação de mensagens enviadas para o URI especial **sip:validar@acme.pt** com um PIN específico, garantindo a segurança.  

## Pontos Incompletos  

- **Erro na Conferência**:
  - Foi desenvolvida a funcionalidade para que o utilizador, no sistema de anúncios **inconference**, possa juntar-se a uma conferência ao introduzir o dígito **0**.  
  - Contudo, ocorre o erro **481**, e o utilizador não consegue juntar-se à conferência.  

---


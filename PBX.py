import sys
import KSR as KSR

def dumpObj(obj):  
    for attr in dir(obj):
        KSR.info("obj attr = %s" % attr)
        if attr != "Status":
            KSR.info(" type = %s\n" % type(getattr(obj, attr)))
        else:
            KSR.info("\n")
    return 1

def mod_init():
    KSR.info("===== from Python mod init\n")
    return Kamailio()

class Kamailio:
    def __init__(self):
        KSR.info('===== Kamailio.__init__\n')
        self.active_sessions = {}
        self.active_conference = []
        self.session_count = 0

    def child_init(self, rank):
        KSR.info('===== Kamailio.child_init(%d)\n' % rank)
        return 0

    def ksr_request_route(self, msg):
        if msg.Method == "REGISTER" and "expires=0" not in KSR.hdr.get("Contact"):
            domain = KSR.pv.get("$rd")
            if domain != "acme.pt":
                KSR.info(f"Reject Register: invalid domain {domain}\n")
                KSR.sl.send_reply(403, "Forbidden: Invalid Domain")
                return 1 
            KSR.info("Register R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.info("        To: " + KSR.pv.get("$tu") +
                     " Contact: " + KSR.hdr.get("Contact") + "\n")
            
            KSR.registrar.save("location", 0)
            state = KSR.registrar.lookup("location")
            KSR.info(f"{print(state)}")
            return 1
        
        if msg.Method == "REGISTER" and "expires=0" in KSR.hdr.get("Contact"):
            KSR.info("Processing deregistration request...\n")
            
            user = KSR.pv.get("$tu")  
            domain = KSR.pv.get("$rd")  
            
            KSR.info(f"Checking registration status for user: {user} in domain: {domain}\n")
            
            if domain == "acme.pt":
                if KSR.registrar.unregister("location", user):
                    KSR.info(f"User {user} deregistered successfully.\n")  
                    KSR.sl.send_reply(200, "Deregistered")  
                else:
                    KSR.info(f"Failed to deregister user: {user}.\n")
                    KSR.sl.send_reply(500, "Internal Server Error")  
            else:
                KSR.info(f"User {user} has an invalid domain: {domain}.\n")
                KSR.sl.send_reply(403, "Forbidden: Invalid Domain")  
            
            return 1

        if msg.Method == "INVITE":
            KSR.info("INVITE R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.info("        From: " + KSR.pv.get("$fu") + " To: " + KSR.pv.get("$tu") + "\n")
            KSR.info(f"{self.active_conference}\n")
            from_domain = KSR.pv.get("$fd")  
            if from_domain != "acme.pt":
                KSR.info(f"Originator with invalid domain: {from_domain}. Rejecting call.\n")
                KSR.sl.send_reply(403, "Forbidden: Invalid Origin Domain")
                return 1
            
            from_address = KSR.pv.get("$fu")
            dest_address = KSR.pv.get("$ru")
            
            if dest_address == "sip:conference@acme.pt":
                KSR.info(f"Starting Conference")
                self.active_conference.append(from_address)
                KSR.rr.record_route()
                KSR.pv.sets("$ru", "sip:conference@127.0.0.1:5090")
                KSR.forward()
                KSR.tm.t_relay()
                return 1
            
            if KSR.registrar.lookup("location") != 1:
                KSR.info(f"Destination {dest_address} is not registered. Rejecting call.\n")
                KSR.sl.send_reply(404, "User Not Registered")
                return 1
            
            if dest_address in self.active_conference:
                KSR.info(f"Destination {dest_address} is busy in a conference. Forwarding to announcements server.\n")
                KSR.rr.record_route()
                KSR.pv.sets("$ru", "sip:inconference@127.0.0.1:5080")
                KSR.forward()
                KSR.tm.t_relay()
                return 1
            
            for session_id, participants in self.active_sessions.items():
                if dest_address in participants:
                    KSR.info(f"Destination {dest_address} is busy in session {session_id}. Forwarding to announcements server.\n")
                    KSR.rr.record_route()
                    KSR.pv.sets("$ru", "sip:busyann@127.0.0.1:5080")
                    KSR.forward() 
                    KSR.tm.t_relay()
                    return 1
            
            
                
            self.session_count += 1
            session_id = f"session{self.session_count}"
            self.active_sessions[session_id] = [from_address, dest_address]
            KSR.info(f"New session created: {session_id} with participants {self.active_sessions[session_id]}\n")
            
            KSR.rr.record_route()
            KSR.tm.t_relay()
            return 1
        
        if msg.Method == "ACK":
            KSR.info("ACK R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.rr.loose_route()
            KSR.tm.t_relay()
            return 1

        if msg.Method == "CANCEL":
            KSR.info("CANCEL R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.registrar.lookup("location")
            KSR.tm.t_relay()
            return 1
        
        if msg.Method == "BYE":
            KSR.info("BYE R-URI: " + KSR.pv.get("$ru") + "\n")
            from_address = KSR.pv.get("$fu")
            dest_address = KSR.pv.get("$ru")
            for session_id, participants in list(self.active_sessions.items()):
                if from_address in participants or dest_address in participants:
                    KSR.info(f"Closing session {session_id} for {participants}\n")
                    del self.active_sessions[session_id]
                    break
            if from_address in self.active_conference:
                KSR.info(f"Leaving conference: {from_address}\n")
                self.active_conference.remove(from_address)
            KSR.rr.loose_route()
            KSR.tm.t_relay()
            return 1
        
        if msg.Method == "INFO":
            sip_body = KSR.pv.get("$rb")
            KSR.info(f"INFO body received: {sip_body}\n")

            for line in sip_body.splitlines():
                if line.startswith("Signal="):
                    signal_value = line.split("Signal=")[-1].strip()
                    KSR.info(f"Parsed signal value: {signal_value}\n")

                    if signal_value == "0":
                        from_address = KSR.pv.get("$fu")
                        KSR.info(f"Key 0 pressed by {from_address}. Redirecting to conference.\n")

                        if from_address not in self.active_conference:
                            self.active_conference.append(from_address)
                        
                        KSR.info("Preparing reINVITE to join conference.\n")
                        KSR.rr.record_route()            
                        KSR.pv.sets("$ru", "sip:conference@127.0.0.1:5090")
                        KSR.pv.sets("$tu", "sip:conference@127.0.0.1:5090")
                        
                        if KSR.tm.t_newtran():  
                            KSR.info("New INVITE sent successfully.\n")
                            KSR.tm.t_relay()  
                        else:
                            KSR.err("Failed to send new INVITE.\n")
                        return 1

                    else:
                        KSR.info("Key pressed is not supported.\n")
                        break
            else:
                KSR.info("No valid Signal= value found in INFO body.\n")
            return 1




        
        if msg.Method == "MESSAGE":
            domain = KSR.pv.get("$rd")
            if domain != "acme.pt":
                KSR.info(f"Originator with invalid domain: {domain}. Rejecting request.\n")
                KSR.sl.send_reply(403, "Forbidden: Invalid Origin Domain")
                return 1
            else:
                if KSR.pv.get("$tu") == "sip:validate@acme.pt":
                    sip_body = KSR.pv.getw("$rb")
                    KSR.info(f"Message body received: {sip_body}\n")
                    
                    if sip_body == "0000":
                        KSR.sl.send_reply(200, "PIN successfully validated")
                    else:
                        KSR.sl.send_reply(403, "Forbidden: Invalid PIN")
                else:
                    KSR.info(f"Message to unknown service: {KSR.pv.get('$tu')}\n")
                    KSR.sl.send_reply(404, "Not Found: Destination service does not exist")
        
    def ksr_reply_route(self, msg):
        KSR.info("===== response - from Kamailio Python script\n")
        status_code = int(KSR.pv.get("$rs"))
        KSR.info("      Status is:{status_code}\n")
        
        if status_code == 486:  
            from_address = KSR.pv.get("$fu") 
            to_address = KSR.pv.get("$tu")    

            KSR.info(f"Removing session with From: {from_address} and To: {to_address} from active_sessions due to 486 status.\n")
            
            for session_id, participants in list(self.active_sessions.items()):
                if from_address in participants or to_address in participants:
                    del self.active_sessions[session_id]
                    KSR.info(f"Session {session_id} removed.\n")
                    break

        return 1

    def ksr_onsend_route(self, msg):
        KSR.info("===== onsend route - from Kamailio Python script\n")
        KSR.info("      %s\n" % (msg.Type))
        return 1

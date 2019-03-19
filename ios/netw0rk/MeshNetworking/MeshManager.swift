//
//  MeshManager.swift
//  netw0rk
//
//  Created by Carlos on 3/12/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import Foundation
import MultipeerConnectivity
import NotificationCenter

class MeshManager: NSObject,MCNearbyServiceAdvertiserDelegate,MCNearbyServiceBrowserDelegate,MCSessionDelegate{
    
    //MARK: Class Variables
    var idToIndex = [String : IndexPath]()
    var advertiser: MCNearbyServiceAdvertiser!
    var browser: MCNearbyServiceBrowser!
    //Uncertain about just using one session and creating a big ole session
    var session: MCSession!
    var peer_id: MCPeerID!
    var devices = [MCPeerID]()
    var sessions = [MCSession]()
    
    init(localName: String){
        super.init()
        self.peer_id = MCPeerID.init(displayName: localName)
        
        //Need to be moved to constants file
        let disc_info = ["name": "netw0rk"]
        let serv_type = "lifeline"
        
        self.advertiser = MCNearbyServiceAdvertiser.init(peer: peer_id, discoveryInfo: disc_info, serviceType: serv_type)
        
        self.browser = MCNearbyServiceBrowser.init(peer: peer_id, serviceType: serv_type)
        
        self.session = MCSession.init(peer: self.peer_id, securityIdentity: nil, encryptionPreference: .none)
        
        self.advertiser.delegate = self
        self.browser.delegate = self
        self.session.delegate = self
    }
    
    
    //MARK: Browser delegate stubs
    func browser(_ browser: MCNearbyServiceBrowser, foundPeer peerID: MCPeerID, withDiscoveryInfo info: [String : String]?) {
        //print("Found Peer with MCPeerID: ",peerID.displayName,"Info: ",info!)
        if !self.devices.contains(peerID){
            self.devices.append(peerID)
            //print("Peers",self.devices)
            //NotificationCenter.default.post(name: NSNotification.Name("updatePeers"), object: nil)
        }
        NotificationCenter.default.post(name: NSNotification.Name("updatePeers"), object: nil)
    }
    
    func browser(_ browser: MCNearbyServiceBrowser, lostPeer peerID: MCPeerID) {
        //print("Lost Peer with MCPeerID: ",peerID.displayName)
        if self.devices.contains(peerID){
            self.devices = self.devices.filter(){ $0 != peerID }
        }
        
        notify(notificationName: "updatePeers", obj: nil)
    }
    
    func browser(_ browser: MCNearbyServiceBrowser, didNotStartBrowsingForPeers error: Error){
        
    }

    
    //MARK: Advertiser delegate stubs
    func advertiser(_ advertiser: MCNearbyServiceAdvertiser, didReceiveInvitationFromPeer peerID: MCPeerID, withContext context: Data?, invitationHandler: @escaping (Bool, MCSession?) -> Void) {
        print("DidRecieveInvitationFrom: ",peerID.displayName)
        
        //Handle peer and add to my session.
        self.idToIndex[peerID.displayName] = IndexPath.init(row: 0, section: 0)
        invitationHandler(true,self.session)
    }
    
    func advertiser(_ advertiser: MCNearbyServiceAdvertiser, didNotStartAdvertisingPeer error: Error){
        print("EEROR", error)
    }
    
    //MARK: Session delegate stubs
    func session(_ session: MCSession, peer peerID: MCPeerID, didChange state: MCSessionState) {
        //let index = self.idToIndex[peerID.displayName]
        switch state{
        case MCSessionState.connected:
            print("Connected to session: \(session)")
            //handle successful connection
            //notify(notificationName: "connected", obj: index! as NSObject)
        case MCSessionState.connecting:
            print("Connecting to session: \(session)")
            //notify(notificationName: "connecting", obj: index! as NSObject)
        default:
            print("Did not connect to session: \(session)")
            //notify(notificationName: "error", obj: index! as NSObject)
        }
    }
    
    func session(_ session: MCSession, didReceive data: Data, fromPeer peerID: MCPeerID) {
        //handle somesort of data
    }
    
    func session(_ session: MCSession, didReceive stream: InputStream, withName streamName: String, fromPeer peerID: MCPeerID) {
        //Handle 1-1 chat
    }
    
    func session(_ session: MCSession, didStartReceivingResourceWithName resourceName: String, fromPeer peerID: MCPeerID, with progress: Progress) {
        //not sure what this is
    }
    
    func session(_ session: MCSession, didFinishReceivingResourceWithName resourceName: String, fromPeer peerID: MCPeerID, at localURL: URL?, withError error: Error?) {
        //What is a resource
    }
    
    //MARK: Class functions
    func start(){
        self.advertiser.startAdvertisingPeer()
        self.browser.startBrowsingForPeers()
    }
    
    func stop(){
        self.advertiser.stopAdvertisingPeer()
        self.browser.stopBrowsingForPeers()
    }
    
    func scan_only(){
        self.browser.startBrowsingForPeers()
    }
    
    func stop_scan_only(){
        self.browser.stopBrowsingForPeers()
    }
    
    func connect(peer_id: MCPeerID,index: IndexPath){
        self.idToIndex[peer_id.displayName] = index
        self.browser.invitePeer(peer_id, to: self.session, withContext: nil, timeout: 0)
    }
    
    func notify(notificationName: String, obj: NSObject?){
        NotificationCenter.default.post(name: NSNotification.Name(notificationName), object: obj)
    }
    
}

//Storing PeerID to localDB
/**
 NSString *displayName = <#Get a name#>;
 
 NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
 NSString *oldDisplayName = [defaults stringForKey:kDisplayNameKey];
 MCPeerID *peerID;
 
 if ([oldDisplayName isEqualToString:displayName]) {
 NSData *peerIDData = [defaults dataForKey:kPeerIDKey];
 peerID = [NSKeyedUnarchiver unarchiveObjectWithData:peerIDData];
 } else {
 peerID = [[MCPeerID alloc] initWithDisplayName:displayName];
 NSData *peerIDData = [NSKeyedArchiver archivedDataWithRootObject:peerID];
 [defaults setObject:peerIDData forKey:kPeerIDKey];
 [defaults setObject:displayName forKey:kDisplayNameKey];
 [defaults synchronize];
 }
 
 **/

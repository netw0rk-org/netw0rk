//
//  meshViewControler.swift
//  netw0rk
//
//  Created by Carlos on 3/8/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import UIKit
import MultipeerConnectivity
import NotificationCenter

class MeshViewController: UIViewController,UITableViewDelegate,UITableViewDataSource,UITextFieldDelegate{
    
    @IBOutlet weak var startMesh: UIButton!
    @IBOutlet weak var stopMesh: UIButton!
    
    @IBOutlet weak var listPeerButtons: UIButton!
    
    @IBOutlet weak var startBrowser: UIButton!
    @IBOutlet weak var stopBrowser: UIButton!
    
    @IBOutlet weak var deviceName: UITextField!
    var meshManager: MeshManager!
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if self.meshManager == nil{
            return 0
            
        }
        else{
            return self.meshManager.devices.count
        }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: "DeviceTableViewCell", for: indexPath) as? DeviceTableViewCell  else {
            fatalError("The dequeued cell is not an instance of DeviceTableViewCell.")}
        
        let device = self.meshManager.devices[indexPath.row]
        // Configure the cell...
        cell.deviceName?.text = device.displayName
        cell.connectionStatus?.text = "👎"
        return cell
    }
    
    @IBOutlet weak var table: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.table.delegate = self
        self.table.dataSource = self
        self.table.layer.borderColor = UIColor.gray.cgColor
        self.table.layer.borderWidth = 1.0
        self.deviceName.delegate = self
        
        NotificationCenter.default.addObserver(self, selector: #selector(reloadTable), name: NSNotification.Name("updatePeers"), object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(connecting), name: NSNotification.Name("connecting"), object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(connected), name: NSNotification.Name("error"), object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(error), name: NSNotification.Name("connected"), object: nil)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
    }
    
    @IBAction func startMesh(_ sender: Any) {
        if !check_name(){
            alert(message: "You must input a device name before you can begin")
            return
        }
        print("Starting Mesh")
        self.meshManager.start()
    }
    @IBAction func stopMesh(_ sender: Any) {
        if !check_name(){ return }
        print("Stopping Mesh")
        self.meshManager.stop()
    }
    
    @IBAction func startScan(_ sender: Any) {
        if !check_name(){
            alert(message: "You must input a device name before you can begin")
            return
        }
        print("Starting Scan")
        self.meshManager.scan_only()
    }
    @IBAction func stopBrowser(_ sender: Any) {
        if !check_name(){ return }
        print("Stopping Scan")
        self.meshManager.stop_scan_only()
    }
    
    //Reload data if MeshDelegate gets new peers or peers leave
    @objc private func reloadTable(){
        self.table.reloadData()
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    //Get input from input boxes and handle appropriatley
    func textFieldDidEndEditing(_ textField: UITextField) {
        let txt = textField.text
        let name = "netw0rk - " + txt!
        self.deviceName.text = name
        self.meshManager = MeshManager.init(localName: name)
    }
    
    func check_name() -> Bool{
        if self.meshManager == nil || self.deviceName.text! == "" {
            return false
        }else{
            return true
        }
    }
    
    func alert(message: String){
        let alertController = UIAlertController(title: "alert", message:
            message, preferredStyle: .alert)
        alertController.addAction(UIAlertAction(title: "Dismiss", style: .default))
        
        self.present(alertController, animated: true, completion: nil)
    }
    
    func tableView(_ tableView: UITableView,
                   didSelectRowAt indexPath: IndexPath){
        let selectedDevice = self.meshManager.devices[indexPath.row]
        //print("Here's: ",name.displayName)
        //<MCPeerID: 0x600002180d70 DisplayName = netw0rk - los>
        
        // send MCPEERID to mesh manager in order to connect
        // Mesh manager should send back a connecting,success or failure connection as a notification,
        // change emoji based on state of device connection
        self.meshManager.connect(peer_id: selectedDevice,index: indexPath)
    }
    
    func updatestatus(state: Int,index: IndexPath){
        DispatchQueue.main.async {
        let cell = self.table.cellForRow(at: index) as! DeviceTableViewCell
        print("Cell",cell)
        switch state{
        case 0:
            cell.connectionStatus.text = "⚙️"
        case 1:
            cell.connectionStatus.text = "❌"
        case 2:
            cell.connectionStatus.text = "✅"
        default:
            print("ERROR switching on status update")
        }
        
        self.table.reloadData()
        }
    }
    
    @objc private func connecting(notification: NSNotification){
        //alert(message: "Connecting")
//        let i = notification.object
//        self.updatestatus(state: 0, index: i as! IndexPath)
    }
    
    @objc private func connected(notification: NSNotification){
        alert(message: "Connected")
//        let i = notification.object
//        self.updatestatus(state: 2, index: i as! IndexPath)
    }
    
    @objc private func error(notification: NSNotification){
        alert(message: "Error")
//        let i = notification.object
//        self.updatestatus(state: 1, index: i as! IndexPath)
    }
    
    @IBAction func listPeers(_ sender: Any) {
        let peers = self.meshManager.session.connectedPeers
        print("\n\nPEERS:",peers)
    }
}

//
//  ViewController.swift
//  netw0rk
//
//  Created by Carlos on 1/31/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import UIKit
import CoreBluetooth
import NotificationCenter

class ViewController: UIViewController,UITextFieldDelegate,UITableViewDataSource,UITableViewDelegate {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.peripheralManager.sigs.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: "SignatureTableViewCell", for: indexPath) as? SignatureTableViewCell  else {
            fatalError("The dequeued cell is not an instance of SignatureViewCell.")}
        
        let sig_data = peripheralManager.sigs[indexPath.row]
        let data_arr  = sig_data.split(separator: "|")
        // Configure the cell...
        cell.signature.text = String(data_arr[0])
        cell.piName.text = String(data_arr[1])
        return cell
    }
    
    
    //MARK: Variables
    
    //Name
    @IBOutlet weak var nameInputBox: UITextField!
    @IBOutlet weak var deviceNameLabel: UILabel!
    //Security Factor
    @IBOutlet weak var securityFactorInput: UITextField!
    @IBOutlet weak var securityFactorLabel: UILabel!
    //Reset
    @IBOutlet weak var resetButton: UIButton!
    @IBOutlet weak var resetTable: UIButton!
    
    @IBOutlet weak var place_holder_pk: UILabel!
    
    //@IBOutlet weak var bleStatus: UILabel!
    
    var peripheralManager: PeripheralManager!
    var user: UserData!
    
    @IBOutlet weak var peripheralSwitch: UISwitch!
    @IBOutlet weak var table: UITableView!
    
    @IBAction func switched(_ sender: Any) {
        if peripheralSwitch.isOn {
            self.peripheralManager.start()
        }else{
            self.peripheralManager.stop()
        }
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        user = UserData("","THIS IS MY PRIVATE KEY MOFO")
        
        nameInputBox.delegate = self
        securityFactorInput.delegate = self
        peripheralManager =  PeripheralManager(user)
        peripheralSwitch.setOn(false, animated: false)
        //bleStatus.text = String(peripheralManager.manager.isAdvertising)
        NotificationCenter.default.addObserver(self, selector: #selector(viewWasLoaded), name: NSNotification.Name("viewLoaded"), object: nil)
        //NotificationCenter.default.addObserver(self, selector: #selector(updateStatus), name: NSNotification.Name("updatestatus"), object: nil)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }
    
    //MARK: Actions
    
    //Clear keyboards when clicking screen
    @IBAction func tapControl(_ sender: UITapGestureRecognizer) {
        nameInputBox.resignFirstResponder()
        securityFactorInput.resignFirstResponder()
    }
    //Clear keyboard when pressing done
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    //Get input from input boxes and handle appropriatley
    func textFieldDidEndEditing(_ textField: UITextField) {
        let txt = textField.text
        
        switch textField{
        case nameInputBox:
            let name = "netw0rk - "+txt!
            deviceNameLabel.text = name
            peripheralManager.data.name = name
        case securityFactorInput:
            securityFactorLabel.text=txt
        default:
            return
        }
    }
    //Reset Everything
    @IBAction func reset(_ sender: UIButton){
            deviceNameLabel.text = "__name__"
            securityFactorLabel.text = "Security Factor"
            nameInputBox.text = ""
            securityFactorInput.text = ""
    }
    
    @IBAction func resetTable(_ sender: Any) {
        self.peripheralManager.sigs.removeAll()
        self.table.reloadData()
    }
    //function that handles notification
    @objc private func viewWasLoaded() {
        self.table.reloadData()
    }
}
    


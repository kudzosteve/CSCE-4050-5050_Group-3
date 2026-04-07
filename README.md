# CSCE-4050-5050_Group-3

## Description
A REST server with one endpoint, “/weather”, that returns a static, hardcoded JSON reply. All task-related screenshots are saved in /Screenshots

## Repository Structure
```text
csce-4050-5050_group-3/
├─Screenshots/
├─client.py
├─README.md
├─requirements.txt
└─server.py
```

## Requirements
```text
- Ubuntu20.04 (SEED Virtual Machine)
- Python3 & pip
- Dependencies ()
```

## Task 1: Setting Up REST Server/Client.

### Wireshark interface before running the server and client program
![Wireshark interface](./Screenshots/wireshark capturing traffic on loopback address.png)

### Running the server

```bash
$ python3 server.py
```

### Terminal output of the server running

![Server running](./Screenshots/server%20running.png)

### Running the client

```bash
$ python3 client.py
```

### Terminal output of the client getting data from the server

![Client getting data](./Screenshots/client%20gets%20data%20from%20the%20server.png)

### Wireshark captured the requests and responses

![Wireshark captured the client-server interaction](./Screenshots/wireshark%20captured%20packets%20between%20server%20and%20client.png)

### HTTP Stream showing the data that the client got from the server

![HTTP Stream showing response](./Screenshots/http%20stream%20showing%20the%20data%20client%20received%20from%20server.png)

## Task 2: Confidentiality and Data Integrity in the Symmetric Setting

After implementing encryption and decryption logics to the project to provide Confidentiality, we used Wireshark to capture the communication between the client and the server.

### Screenshot showing the server running

![Server running](./Screenshots/server%20running_2.png)

### Screenshot showing the client getting the data in plaintext

![Client recieves data](./Screenshots/client%20gets%20data%20from%20the%20server_2.png)

### Wireshark captured client-server communication

![Wireshark captured encrypted communication](./Screenshots/Wireshark%20intercepted%20commincation%20between%20client%20server.png)

### HTTP Stream showing the encrypted data that the client received

![HTTP stream shows encrypted data](./Screenshots/HTTP%20stream%20shows%20the%20encrypted%20data.png)

## Task 3

Run the server using: python server_kx.py
Client: client_kx.py

### Screen showing the generated keys and the server running afterwards

![Key pair and server running](./Screenshots/3_key%20pair%20generated%20and%20server%20running.png)

### Screenshot showing the client getting the data in plaintext

![Client retrieves data](./Screenshots/3_client%20gets%20the%20data%20in%20plaintext.png)

### HTTP Stream showing the server's public key

![Server's public key](./Screenshots/3_HTTP%20stream%20shows%20server's%20public%20key.png)

### HTTP Stream showing the client's encrypted session key

![Encrypted session key](./Screenshots/3_HTTP%20stream%20shows%20encrypted%20session%20key.png)

### HTTP Stream showing the encrypted data and the signature

![Encrypted data and signature](./Screenshots/3_HTTP%20stream%20shows%20encrypted%20data%20and%20signature.png)

## Task 4

To run the server use: python server_ca.py
To run the client use: python client_ca.py
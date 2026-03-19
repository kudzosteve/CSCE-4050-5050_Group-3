# CSCE-4050-5050_Group-3

## Description
A REST server with one endpoint, “/weather”, that returns a static, hardcoded JSON reply.

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

## Note

The repository will be updated as the project progresses.
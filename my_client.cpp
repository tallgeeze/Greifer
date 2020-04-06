#include<iostream>
#include<string>
#include<winsock.h>
#pragma comment(lib,"ws2_32.lib")
using namespace std;
void initialization();
int main() {

	//Laenge der Daten begrenzen
	int send_len = 4096;
	int recv_len = 4096;

	// Die Groesse der Buffer eingeben
	char send_buf[1000];
	char recv_buf[1000];

	//s_server : die Entitaet der Server Socket
	SOCKET s_server;
	//server_addr: Die Informationsstruktur der Adresse und Port
	SOCKADDR_IN server_addr;

	initialization();

	char  temp[1000]="";
	int target_port;
Label1:
	cout << "Bitte die IP Adresse eingeben:" << endl;
	std::cin.getline(temp, sizeof temp);
	cout << "Bitte die Port Nummer eingeben" << endl;
	cin >> target_port;

	//IP-Adresse und Port nummer eingeben. In server_addr(Struktur: SOCKADDR_IN)
	server_addr.sin_family = AF_INET; 
	server_addr.sin_addr.S_un.S_addr = inet_addr(temp); // IP Adresse des Server
	//server_addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1"); // IP Adresse des Server
	server_addr.sin_port = htons(target_port); //Port Definition


	//Die IP-Adresse und Port Information in s_server(ein Object der socket Struktur)
	s_server = socket(AF_INET, SOCK_STREAM, 0);
	//cout << "SOCKETADDR_LENGTH=" << sizeof(SOCKADDR);
	//versuchen, Verbindung zu erstellen 
	// connect(para1--class SOCKET instance,  para2-- class SOCKADDR instance, para3-- length of SOCKADDR 
	if (connect(s_server, (SOCKADDR *)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		cout << "Verbindung nicht erfolgreich gestellte" << endl;
		goto Label1;
		WSACleanup();
	}
	else {
		cout << "Verbindung erfolgreich gestellte£¡" << endl;
	}



	//Empfehlen und abschicken
	while (1) {
		cout << "\nClient:";
		cin >> send_buf;
		cout << "\n" << endl;
		send_len = send(s_server, send_buf, 100, 0);
		if (send_len < 0) {
			cout << "Etwas beim Abschick hat falschgeschlagen" << endl;
			break;
		}
		recv_len = recv(s_server, recv_buf, 100, 0);
		if (recv_len < 0) {
			cout << "Paket ist verloren in Uebertragung" << endl;
			break;
		}
		else {
			cout << "Server:" << recv_buf << endl;
		}
		if (recv_buf == "CMD_CHANGESOCKET") { goto Label1; }

	}
	//Socket abschliessen
	closesocket(s_server);
	//Resourcen loslassen
	WSACleanup();
	return 0;
}
void initialization() {
	
	WORD w_req = MAKEWORD(2, 2);//Version eingeben
	WSADATA wsadata;
	int err;
	err = WSAStartup(w_req, &wsadata);
	if (err != 0) {
		cout << "Initialization nicht erfolgreich" << endl;
	}
	else {
		cout << "Initialization erfolgreich" << endl;
	}


	//Version ueberpruefen
	if (LOBYTE(wsadata.wVersion) != 2 || HIBYTE(wsadata.wHighVersion) != 2) {
		cout << "nicht richtig Version" << endl;
		WSACleanup();
	}
	else {
		cout << "richtig Version" << endl;
	}


}

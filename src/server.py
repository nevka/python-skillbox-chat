#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
#  Ctrl + Alt + L - форматирование кода
#
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None
    logins: list = []
    history_list: list = []

    def connectionMade(self):
        # Потенциальный баг для внимательных =)
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def lineReceived(self, line: bytes):
        content = line.decode()

        if self.login is not None:
            content = f"Message from {self.login}: {content}"
            self.add_history(content)
            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(content.encode())
        else:
            # login:admin -> admin
            if content.startswith("login:"):
                self.login = content.replace("login:", "")
                if self.login:
                    if self.login in self.logins:
                        # кириллица на windows 10 кракозябры показывает, поэтому...
                        self.sendLine(f"This login {self.login} used".encode())
                    else:
                        self.send_history()
                        self.logins.append(self.login)
                        self.sendLine(f"Welcome {self.login}!".encode())
            else:
                self.sendLine("Invalid login".encode())

    def send_history(self):
        if self.history_list:
            for msg in self.history_list:
                self.sendLine(msg.encode())

    def add_history(self, msg):
        if len(self.history_list) >= 10:
            del self.history_list[0]
        self.history_list.append(msg)


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list

    def startFactory(self):
        self.clients = []
        print("Server started")

    def stopFactory(self):
        print("Server closed")


reactor.listenTCP(1234, Server())
reactor.run()

#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Работа с функциями, аргументы и возвращаемое значение
#

original_users = ["Artur", "John", "Jack"]


def print_users(users):
    for user in users:
        print("Hello, " + user)


another_users = ["Kate", "Gatlin", "Chris"]

print_users(original_users)
print_users(another_users)

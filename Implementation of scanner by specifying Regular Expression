//**Implementation of scanner by specifying Regular Expressions**//


#include <stdio.h>
#include <stdlib.h>
#include <regex.h>

#define MAX_MATCHES 10
#define MAX_MATCH_LENGTH 100

int main() {
    // Define the regular expressions for tokens
    regex_t regex_identifier, regex_integer, regex_float;
    regcomp(&regex_identifier, "[a-zA-Z][a-zA-Z0-9_]*", REG_EXTENDED);
    regcomp(&regex_integer, "[0-9]+", REG_EXTENDED);
    regcomp(&regex_float, "[0-9]+\\.[0-9]+", REG_EXTENDED);

    char input[MAX_MATCH_LENGTH];
    printf("Enter input: ");
    fgets(input, sizeof(input), stdin);

    // Scan the input and match against the regular expressions
    regmatch_t matches[MAX_MATCHES];
    while (input[0] != '\0') {
        if (regexec(&regex_identifier, input, MAX_MATCHES, matches, 0) == 0) {
            printf("Identifier: %.*s\n", (int)(matches[0].rm_eo - matches[0].rm_so), &input[matches[0].rm_so]);
        } else if (regexec(&regex_integer, input, MAX_MATCHES, matches, 0) == 0) {
            printf("Integer: %.*s\n", (int)(matches[0].rm_eo - matches[0].rm_so), &input[matches[0].rm_so]);
        } else if (regexec(&regex_float, input, MAX_MATCHES, matches, 0) == 0) {
            printf("Float: %.*s\n", (int)(matches[0].rm_eo - matches[0].rm_so), &input[matches[0].rm_so]);
        } else {
            printf("Unexpected token: %c\n", input[0]);
            input++;
        }

        // Move to the next token
        input += matches[0].rm_eo;
    }

    // Free the compiled regular expressions
    regfree(&regex_identifier);
    regfree(&regex_integer);
    regfree(&regex_float);

    return 0;
}



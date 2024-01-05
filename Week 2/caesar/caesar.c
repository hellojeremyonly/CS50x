#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2) {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    // Make sure every character in argv[1] is a digit
    for (int i = 0, n = strlen(argv[1]); i < n; i++) {
        if (!isdigit(argv[1][i])) {
            printf("Usage: ./caesar k\n");
            return 1;
        }
    }
    // Convert argv[1] from a `string` to an `int`
    int k = atoi(argv[1]);
    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    // For each character in the plaintext:
    printf("ciphertext: ");
        // Rotate the character if it's a letter
        for (int i = 0, n = strlen(plaintext); i < n; i++) {
            if (isalpha(plaintext[i])) {
                // Rotate lowercase letters
                if (islower(plaintext[i])) {
                    printf("%c", (((plaintext[i] - 97) + k) % 26) + 97);
                }
                // Rotate uppercase letters
                else if (isupper(plaintext[i])) {
                    printf("%c", (((plaintext[i] - 65) + k) % 26) + 65);
                }
            }
            // Print the character if it's not a letter
            else {
                printf("%c", plaintext[i]);
            }
        }
    printf("\n");
    return 0;
}

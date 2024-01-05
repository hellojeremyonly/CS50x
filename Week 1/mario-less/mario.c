#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt user for height of pyramid
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Print out pyramid
    for (int i = 1; i <= height; i++)
    {
        // Print spaces
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        // Print hashes
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }

        // Print newline character
        printf("\n");
    }
}

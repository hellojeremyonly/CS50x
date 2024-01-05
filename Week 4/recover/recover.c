#include <stdio.h>
#include <stdlib.h>

#define JPEG_SIG_SIZE 4
#define BLOCK_SIZE 512
#define MAX_FILENAME_SIZE 8

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    unsigned char buffer[BLOCK_SIZE];
    FILE *current_file = NULL;
    int file_number = 0;
    char filename[MAX_FILENAME_SIZE];

    while (fread(buffer, BLOCK_SIZE, 1, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (current_file != NULL)
            {
                fclose(current_file);
            }

            sprintf(filename, "%03i.jpg", file_number++);
            current_file = fopen(filename, "w");
        }

        if (current_file != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, current_file);
        }
    }

    if (current_file != NULL)
    {
        fclose(current_file);
    }

    fclose(file);

    return 0;
}
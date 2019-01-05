#include <byteswap.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int usage_info(void)
{
	printf("ti-bt.c -- resolves Bluetooth MAC from Wifi MAC\n");
	printf("./ti-bt\t<MAC ADDR>\n");
	return 1;
}

int main(int argc, char **argv)
{
	/*TODO: add changing of 0x14 to arbitrary */
	const unsigned short fourteen = 20;
	unsigned short subtractor = 2;
	unsigned short octets[6];
	unsigned short out_octets[6];

	if (argc < 2) {
		printf("not enough args.\n");
		return usage_info();
	}
	else if (argc >= 3) {
		subtractor = (unsigned short) atoi(argv[2]);
	}

	if (strchr(argv[1], ':') == NULL) {
		printf("NOT A MAC. :-?\n");
		return usage_info();
	}

	if (strlen(argv[1])+1 < 18) {
		return usage_info();
	}

	memset(&out_octets, '\0', sizeof(out_octets));
	memset(&octets, '\0', sizeof(octets));
	sscanf(argv[1], "%2x%*c%2x%*c%2x%*c%2x%*c%2x%*c%2x", &octets[0],
		&octets[1], &octets[2], &octets[3], &octets[4],
		&octets[5]);

	/* is first octet 0x7X? AND is NOT eq to 0x71  *
         * must be in range of 0x72 to 0x76            */
	unsigned short first = octets[0]&127;
	unsigned short index = 0;
	unsigned short bswap_me = 0;
	unsigned short oct_x = 0;
	unsigned short oct_x_1 = 0;
	unsigned short oct_x_2 = 0;
	signed short post_fourt = 0;
	if ((octets[0] ^ 113) == 0 || first>>4 != 7 || octets[0] > 118) {
		printf("invalid mac.\n");
		return usage_info();
	}
	first = octets[0]-2;
	/* OCTET 1 - 2 must be >= 0x72 */
	if (first < 114) {
		printf("invalid mac.\n");
		return usage_info();
	}		
	index = 0x0F&octets[0]-1;
	/* let OCTET 1's lower 4bits as x, OCTET x == 0x14 *
         * 	otherwise fail                             */
	if (octets[index] != fourteen) {
		printf("MAC[%d] != %X\n", index, fourteen);
		return usage_info();
	}
	/* byteswap an octet, its going to be subtracted from OCTET5 */
	if (index <= 2) {
		bswap_me = bswap_16(octets[index+1])|octets[index+1];
		bswap_me = bswap_me&0x0FF0;
		bswap_me >>= 4;
	} else {
		bswap_me = bswap_16(octets[index-1])|octets[index-1];
		bswap_me = bswap_me&0x0FF0;
		bswap_me >>= 4;
	}
	oct_x = octets[index+1];
	oct_x_2 = oct_x-bswap_me;
	oct_x_2 = oct_x_2-++index;
	oct_x_1 = oct_x-oct_x_2;

	/*
	 * FIXME: THIS IS MISSING STUFF FOR VARIANT POS. OF 14 but w/e
	 */
	post_fourt = (signed short)octets[1] - (signed short)octets[5];
	int i;
	double d = 0.0;
	for (i = 0; i < 6; i++) {
		d = (double)octets[i];
		if (d == fmax((double)octets[1],(double)octets[5])) {
			post_fourt = post_fourt - (signed short) i-1;
			break;
		}
	}
	
	/* start building output */
	out_octets[5] = oct_x_2;
	out_octets[4] = oct_x_1;
	out_octets[3] = bswap_me;
	out_octets[2] = (unsigned short) post_fourt & 0x00FF;
	out_octets[1] = fourteen;
	out_octets[0] = octets[0]-subtractor;

	printf("%X:%X:%X:%X:%2X:%X\n", out_octets[0], out_octets[1],
		out_octets[2], out_octets[3], out_octets[4], out_octets[5]);
	
	return 0;
}

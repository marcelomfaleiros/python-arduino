int newport_cal[740] = {200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 218,
                219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238,
                239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257,
                258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277,
                278, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296,
                297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 308, 309, 310, 311, 312, 313, 314, 315,
                316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335,
                336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 348, 349, 350, 351, 352, 353, 354,
                355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374,
                375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 390, 391, 392, 393,
                394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413,
                414, 415, 416, 417, 418, 419, 420, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432,
                433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 443, 444, 445, 446, 447, 448, 449, 440, 451,
                452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471,
                472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 486, 487, 488, 489, 490,
                491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510,
                511, 512, 513, 514, 515, 516, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529,
                530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 548,
                549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568,
                569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587,
                588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607,
                608, 609, 610, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626,
                627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 643, 644, 645,
                646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665,
                666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 678, 679, 680, 681, 682, 683, 684,
                685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704,
                705, 706, 707, 708, 709, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723,
                724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743,
                744, 745, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762,
                763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 779, 780, 781,
                782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 
                802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821,
                822, 823, 824, 825, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 
                841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 852, 853, 854, 855, 856, 857, 858, 859,
                860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879,
                880, 881, 882, 882, 883, 884, 885, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 
                898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917};


int currpos = 200;
int k, nm, wl, wls, display_pos;

void clockwise(void);
void anticlockwise(void);
void disable(void);

void setup() 
{ 
  Serial.begin(9600);  
  pinMode(8, OUTPUT); // Configura os pinos d8, 
  pinMode(9, OUTPUT); // d9, 
  pinMode(10, OUTPUT);// d10 e 
  pinMode(11, OUTPUT);// d11 como saídas
}

void loop() 
{                        
  while (Serial.available() > 0)   //verifica a porta serial 
  {             
    wls = Serial.parseInt();   //recebe um valor via serial em nm        
    nm = newport_cal[wls-200] - currpos;    
    if (nm > 0 && wls >0)    
    {                        
      for(k = 0; k < nm; k++) 
        {  
           clockwise();  
           wl = currpos + 1 + k;
           Serial.println(wl);
        }
    currpos = newport_cal[wls-200];      
    }               
    else if (nm < 0 && wls > 0)
    {                      
      for(k = 0; k < (abs(nm) + 5); k++) 
        {  
           anticlockwise();   
           wl = currpos -  1 - k;
           Serial.println(wl);
        }
      for (k = 0; k < 5; k++) 
        {  
           clockwise();  
           wl = wl  + 1 +  k;
           Serial.println(wl); 
        }
    currpos = newport_cal[wls-200];
    }  
    else if (wls = 0)
    {
      disable();
    }  
   }
}    
  
void clockwise()
{ 
  int i = 0;
  while(i <= 20)
  {
    digitalWrite(8, HIGH);    // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);    // Configura o pino 9 como LOW  
    digitalWrite(10, LOW);    // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);    // Configura o pino 11 como LOW  
    delay(4);                   // Espera 4 ms
    digitalWrite(8, LOW);     // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);    // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH);   // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);    // Configura o pino 11 como LOW  
    delay(4);                   // Espera 4 ms
    digitalWrite(8, LOW);     // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);     // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH);   // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH);   // Configura o pino 11 como LOW
    delay(4);                   // Espera 4 ms 
    digitalWrite(8, HIGH);    // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);     // Configura o pino 9 como LOW  
    digitalWrite(10, LOW);    // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH);   // Configura o pino 11 como LOW
    delay(4);                   // Espera 4 ms
    i = i + 1;
  }
}

void anticlockwise()
{
  int j = 0;
  while(j <= 20)
  {
    digitalWrite(8, HIGH);  // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);   // Configura o pino 9 como LOW  
    digitalWrite(10,LOW);  // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH); // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms
    digitalWrite(8, LOW);   // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);   // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH); // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms
    digitalWrite(8, LOW);   // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);  // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);  // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms 
    digitalWrite(8, HIGH);  // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);  // Configura o pino 9 como LOW  
    digitalWrite(10, LOW);  // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);  // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms
    j = j + 1;
  }
}

void disable()
{
  digitalWrite(8, HIGH);  // Configura o pino 8 como HIGH              
  digitalWrite(9, LOW);   // Configura o pino 9 como LOW  
  digitalWrite(10, LOW);  // Configura o pino 10 como HIGH                
  digitalWrite(11, LOW); // Configura o pino 11 como LOW
}

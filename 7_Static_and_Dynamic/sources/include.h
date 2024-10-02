/**
 * Polyspace example.
 *       Copyright 2012-2023 The MathWorks, Inc.
 */

#ifndef INCLUDE_H
#define INCLUDE_H

#define new_move 0
#define previous_move 1

#define MAX_SIZE 10

extern void SEND_MESSAGE(int status, const char* message);
extern int read_bus_status(void);
extern int read_on_bus(void);

extern void initialise_current_data(void);
extern void compute_new_coordonates(void);
extern void sort_calibration(void);
extern int polynomia(int input);

extern int random_int(void);
extern float random_float(void);
extern void partial_init(int* new_alt);
extern void RTE(void);
extern void Exec_One_Cycle(int);
extern int orderregulate(void);
extern void Begin_CS(void);
extern void End_CS(void);
extern void Increase_PowerLevel(void);
extern int Get_PowerLevel(void);
extern void Compute_Injection(void);

extern int tab[MAX_SIZE];
extern int PowerLevel;
extern int first_payload;
extern int second_payload;
extern int* arr;

#endif

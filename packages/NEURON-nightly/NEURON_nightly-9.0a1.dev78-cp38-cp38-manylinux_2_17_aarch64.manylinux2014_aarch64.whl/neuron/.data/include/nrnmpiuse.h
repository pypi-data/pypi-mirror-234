#ifndef usenrnmpi_h
#define usenrnmpi_h

/* define to 1 if you want MPI specific features activated */
#define NRNMPI 1

/* define to 1 if you want mpi dynamically loaded instead of linked normally */
#define NRNMPI_DYNAMICLOAD 1

/* define to 1 if you want the MUSIC - MUlti SImulation Coordinator */
/* #undef NRN_MUSIC */

/* define to the dll path if you want to load automatically */
#define DLL_DEFAULT_FNAME "aarch64/.libs/libnrnmech.so"

/* define if needed */
/* #undef ALWAYS_CALL_MPI_INIT */

/* Number of times to retry a failed open */
/* #undef FILE_OPEN_RETRY */

#endif

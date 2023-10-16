/* config.h.in.  Generated from configure.ac by autoheader.  */


#ifndef H_nrnconf_included
#define H_nrnconf_included 1


/* Define if building universal (internal helper macro) */
/* #undef AC_APPLE_UNIVERSAL_BUILD */

/* Define to one of `_getb67', `GETB67', `getb67' for Cray-2 and Cray-YMP
   systems. This function is required for `alloca.c' support on those systems.
   */
/* #undef CRAY_STACKSEG_END */

/* if mac os x */
/* #undef DARWIN */

/* Define to 1 if you have the `bcopy' function. */
#define HAVE_BCOPY 1

/* Define to 1 if you have the `bzero' function. */
#define HAVE_BZERO 1

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the <execinfo.h> header file. */
#define HAVE_EXECINFO_H 1

/* Define to 1 if you have the <fenv.h> header file. */
#define HAVE_FENV_H 1

/* Define to 1 if you have the `fesetround' function. */
#define HAVE_FESETROUND 1

/* Define to 1 if you have the `feenableexcept' function. */
#define HAVE_FEENABLEEXCEPT 1

/* Define to 1 if you have the `gettimeofday' function. */
#define HAVE_GETTIMEOFDAY 1

/* Define to 1 if you have the `index' function. */
#define HAVE_INDEX 1

/* Define to 1 if you have the `isatty' function. */
#define HAVE_ISATTY 1

/* define if using InterViews */
#define HAVE_IV 1

/* Define to 1 if you have the `mallinfo' function. */
#define HAVE_MALLINFO 1

/* Define to 1 if you have the `mallinfo2' function. */
/* #undef HAVE_MALLINFO2 */

/* Define to 1 if you have the <malloc.h> header file. */
#define HAVE_MALLOC_H 1

/* Define to 1 if you have the `mkstemp' function. */
#define HAVE_MKSTEMP 1

/* Define to 1 if you have the `posix_memalign' function. */
#define HAVE_POSIX_MEMALIGN 1

/* Define to 1 if you have the `realpath' function. */
#define HAVE_REALPATH 1

/* Define to 1 if you have the `setenv' function. */
#define HAVE_SETENV 1

/* Define to 1 if you have the `setitimer' function. */
#define HAVE_SETITIMER 1

/* Define to 1 if you have the `sigaction' function. */
#define HAVE_SIGACTION 1

/* Define to 1 if you have the `sigprocmask' function. */
#define HAVE_SIGPROCMASK 1

/* (Define if this signal exists) */
#define HAVE_SIGBUS 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* define if using mingw */
/* #undef MINGW */

/* define if using Mike Neubig <neubig@salk.edu> contributions */
/* #undef MikeNeubig */

/* where the lib hoc is */
#define NEURON_DATA_DIR "/root/nrn/build/cmake_install/share/nrn"

/* host triplet */
#define NRNHOST "aarch64-Linux"

/* if 1 then dlopen nrnmech instead of special */
#define NRNMECH_DLL_STYLE 1

/* if 1 then dynamic units default is legacy units */
/* #undef DYNAMIC_UNITS_USE_LEGACY_DEFAULT */

/* if nrnoc can use X11 */
#define NRNOC_X11 1

/* location of NEURON libraries */
#define NRN_LIBDIR "/root/nrn/build/cmake_install/lib"

/* Name of package */
#define PACKAGE "nrn"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT ""

/* Define to the full name of this package. */
/* #undef PACKAGE_NAME */

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "nrn 9.0.0"

/* Define to the one symbol short name of this package. */
/* #undef PACKAGE_TARNAME */

/* Define to the home page for this package. */
#define PACKAGE_URL ""

/* Define to the version of this package. */
#define PACKAGE_VERSION "9.0.0"

/* Define as the return type of signal handlers (`int' or `void'). */
#define RETSIGTYPE void

/* define if RETSIGTYPE(*)(int) is not the prototype for a signal handler */
/* #undef SIGNAL_CAST */

/* If using the C implementation of alloca, define if you know the
   direction of stack growth for your system; otherwise it will be
   automatically deduced at runtime.
	STACK_DIRECTION > 0 => grows toward higher addresses
	STACK_DIRECTION < 0 => grows toward lower addresses
	STACK_DIRECTION = 0 => direction of growth unknown */
/* #undef STACK_DIRECTION */

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Define SUNDIALS data type 'realtype' as 'long double' */
#define SUNDIALS_DOUBLE_PRECISION 1

/* Use generic math functions */
#define SUNDIALS_USE_GENERIC_MATH 1

/* Define to 1 if you can safely include both <sys/time.h> and <time.h>. */
#define TIME_WITH_SYS_TIME 1

/* Define to 1 if your <sys/time.h> declares `struct tm'. */
/* #undef TM_IN_SYS_TIME */

/* Version number of package */
#define VERSION "9.0.0"

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most
   significant byte first (like Motorola and SPARC, unlike Intel). */
#if defined AC_APPLE_UNIVERSAL_BUILD
# if defined __BIG_ENDIAN__
#  define WORDS_BIGENDIAN 1
# endif
#else
# ifndef WORDS_BIGENDIAN
#  undef WORDS_BIGENDIAN
# endif
#endif

/* Define to 1 if the X Window System is missing or not being used. */
/* #undef X_DISPLAY_MISSING */

/* Define to 1 if `lex' declares `yytext' as a `char *' by default, not a
   `char[]'. */
#define YYTEXT_POINTER 1

/* Define to the type of a signed integer type of width exactly 64 bits if
   such a type exists and the standard includes do not define it. */
/* #undef int64_t */

/* Define to `long int' if <sys/types.h> does not define. */
/* #undef off_t */

/* Define to `int' if <sys/types.h> does not define. */
/* #undef pid_t */

/* Define to `unsigned int' if <sys/types.h> does not define. */
/* #undef size_t */

/* __cplusplus guard still needed because this header is included from C code in
 * mesch (and maybe others)
 */
#if defined(__cplusplus)
#include <array>
#include <string_view>
namespace neuron::config {
#ifdef USE_PYTHON
   constexpr std::string_view default_python_executable{R"(/root/nrn/nrn_build_venv39_76095312/bin/python)"};
   constexpr std::array<std::string_view, 1> supported_python_versions{"3.9"};
#endif
   constexpr std::string_view shared_library_prefix{"lib"};
   constexpr std::string_view shared_library_suffix{".so"};
   constexpr std::string_view system_processor{"aarch64"};
}
#endif

#ifdef MINGW
#define WIN32 1
#endif

#endif /* H_nrnconf_included */


#pragma once

// #include <stdio.h>
#include <stdexcept>

#include <warpat/cuda.h>

#include <iostream>

#ifndef CUDA_ERROR_CHECK
#define CUDA_ERROR_CHECK(ans) { CUDA_ASSERT((ans), __FILE__, __LINE__); }
#endif

inline void CUDA_ASSERT(CUresult code, const char *file, int line, bool abort=true)
{
   if (code != CUDA_SUCCESS) 
   {
      const char* errorString = nullptr;
      cuGetErrorString(code, &errorString);
      // fprintf(stderr,"CUDA_ASSERT: %s in %s at line:%d\n", errorString, file, line);
      std::cerr << "CUDA_ASSERT: " << errorString << " in " << file << " at line:" << line << std::endl;
      if (abort) exit(code);
   }
}


inline void CUDA_ASSERT_EX(CUresult code, const char *file, int line,  const char *message, bool abort=true)
{
   if (code != CUDA_SUCCESS) 
   {
      const char* errorString = nullptr;
      cuGetErrorString(code, &errorString);
      // fprintf(stderr,"CUDA_ASSERT: %s in %s at line:%d\n", errorString, file, line, message);
      std::cerr << "CUDA_ASSERT: " << errorString << " in " << file << " at line:" << line << std::endl;
      if (abort) exit(code);
   }
}

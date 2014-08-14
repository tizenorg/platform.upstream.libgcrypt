/* hwf-arm.c - Detect hardware features - ARM part
 * Copyright © 2013  Jussi Kivilinna <jussi.kivilinna@iki.fi>
 *
 * This file is part of Libgcrypt.
 *
 * Libgcrypt is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 2.1 of
 * the License, or (at your option) any later version.
 *
 * Libgcrypt is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; if not, see <http://www.gnu.org/licenses/>.
 */

#include <config.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>

#include "g10lib.h"
#include "hwf-common.h"

#if !defined (__arm__)
# error Module build for wrong CPU.
#endif

#undef HAS_SYS_AT_HWCAP
#ifdef __linux__

#define HAS_SYS_AT_HWCAP 1

#define AT_HWCAP 16
#define HWCAP_NEON 4096

static int
get_hwcap(unsigned int *hwcap)
{
  struct { unsigned int a_type; unsigned int a_val; } auxv;
  FILE *f;
  int err = -1;
  static int hwcap_initialized = 0;
  static unsigned int stored_hwcap;

  if (hwcap_initialized)
    {
      *hwcap = stored_hwcap;
      return 0;
    }

  f = fopen("/proc/self/auxv", "r");
  if (!f)
    {
      *hwcap = stored_hwcap;
      return -1;
    }

  while (fread(&auxv, sizeof(auxv), 1, f) > 0)
    {
      if (auxv.a_type != AT_HWCAP)
        continue;

      stored_hwcap = auxv.a_val;
      hwcap_initialized = 1;
      err = 0;
      break;
    }

  fclose(f);
  *hwcap = stored_hwcap;
  return err;
}

static unsigned int
detect_arm_at_hwcap(void)
{
  unsigned int hwcap;
  unsigned int features = 0;

  if (get_hwcap(&hwcap) < 0)
    return features;

#ifdef ENABLE_NEON_SUPPORT
  if (hwcap & HWCAP_NEON)
    features |= HWF_ARM_NEON;
#endif

  return features;
}

#endif /* __linux__ */

unsigned int
_gcry_hwf_detect_arm (void)
{
  unsigned int ret = 0;

#if defined (HAS_SYS_AT_HWCAP)
  ret |= detect_arm_at_hwcap ();
#else
  ret |= 0;
#endif

#if defined(__ARM_NEON__) && defined(ENABLE_NEON_SUPPORT)
  ret |= HWF_ARM_NEON;
#endif

  return ret;
}

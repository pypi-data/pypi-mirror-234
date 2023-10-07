/**
  @file

  @ingroup cudd

  @brief Functions that translate BDDs to ZDDs.

  @author Hyong-kyoon Shin, In-Ho Moon

  @copyright@parblock
  Copyright (c) 1995-2015, Regents of the University of Colorado

  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:

  Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

  Neither the name of the University of Colorado nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE.
  @endparblock

*/

#include "util.h"
#include "cuddInt.h"

/*---------------------------------------------------------------------------*/
/* Constant declarations                                                     */
/*---------------------------------------------------------------------------*/


/*---------------------------------------------------------------------------*/
/* Stucture declarations                                                     */
/*---------------------------------------------------------------------------*/


/*---------------------------------------------------------------------------*/
/* Type declarations                                                         */
/*---------------------------------------------------------------------------*/


/*---------------------------------------------------------------------------*/
/* Variable declarations                                                     */
/*---------------------------------------------------------------------------*/


/*---------------------------------------------------------------------------*/
/* Macro declarations                                                        */
/*---------------------------------------------------------------------------*/

/** \cond */

/*---------------------------------------------------------------------------*/
/* Static function prototypes                                                */
/*---------------------------------------------------------------------------*/

static DdNode * zddPortFromBddStep (DdManager *dd, DdNode *B, int expected);
static DdNode * zddPortToBddStep (DdManager *dd, DdNode *f, int depth);

/** \endcond */


/*---------------------------------------------------------------------------*/
/* Definition of exported functions                                          */
/*---------------------------------------------------------------------------*/


/**
  @brief Converts a %BDD into a %ZDD.

  @details This function assumes that there is a one-to-one
  correspondence between the %BDD variables and the %ZDD variables, and
  that the variable order is the same for both types of
  variables. These conditions are established if the %ZDD variables are
  created by one call to Cudd_zddVarsFromBddVars with multiplicity = 1.

  @return a pointer to the resulting %ZDD if successful; NULL otherwise.

  @sideeffect None

  @see Cudd_zddVarsFromBddVars

*/
DdNode *
Cudd_zddPortFromBdd(
  DdManager * dd,
  DdNode * B)
{
    DdNode *res;

    do {
	dd->reordered = 0;
	res = zddPortFromBddStep(dd,B,0);
    } while (dd->reordered == 1);
    if (dd->errorCode == CUDD_TIMEOUT_EXPIRED && dd->timeoutHandler) {
        dd->timeoutHandler(dd, dd->tohArg);
    }

    return(res);

} /* end of Cudd_zddPortFromBdd */


/**
  @brief Converts a %ZDD into a %BDD.

  @return a pointer to the resulting %ZDD if successful; NULL
  otherwise.

  @sideeffect None

  @see Cudd_zddPortFromBdd

*/
DdNode *
Cudd_zddPortToBdd(
  DdManager * dd,
  DdNode * f)
{
    DdNode *res;

    do {
	dd->reordered = 0;
	res = zddPortToBddStep(dd,f,0);
    } while (dd->reordered == 1);
    if (dd->errorCode == CUDD_TIMEOUT_EXPIRED && dd->timeoutHandler) {
        dd->timeoutHandler(dd, dd->tohArg);
    }

    return(res);

} /* end of Cudd_zddPortToBdd */


/*---------------------------------------------------------------------------*/
/* Definition of internal functions                                          */
/*---------------------------------------------------------------------------*/

/*---------------------------------------------------------------------------*/
/* Definition of static functions                                            */
/*---------------------------------------------------------------------------*/


/**
  @brief Performs the recursive step of Cudd_zddPortFromBdd.

  @sideeffect None

*/
static DdNode *
zddPortFromBddStep(
  DdManager * dd,
  DdNode * B,
  int  expected)
{
    DdNode	*res, *prevZdd, *t, *e;
    DdNode	*Breg, *Bt, *Be;
    int		id;
    int		level;

    statLine(dd);
    /* Terminal cases. */
    if (B == Cudd_Not(DD_ONE(dd)))
	return(DD_ZERO(dd));
    if (B == DD_ONE(dd)) {
	if (expected >= dd->sizeZ) {
	    return(DD_ONE(dd));
	} else {
	    return(dd->univ[expected]);
	}
    }

    Breg = Cudd_Regular(B);

    /* Computed table look-up. */
    res = cuddCacheLookup1Zdd(dd,Cudd_zddPortFromBdd,B);
    if (res != NULL) {
	level = cuddI(dd,Breg->index);
	/* Adding DC vars. */
	if (expected < level) {
	    /* Add suppressed variables. */
	    cuddRef(res);
	    for (level--; level >= expected; level--) {
		prevZdd = res;
		id = dd->invperm[level];
		res = cuddZddGetNode(dd, id, prevZdd, prevZdd);
		if (res == NULL) {
		    Cudd_RecursiveDerefZdd(dd, prevZdd);
		    return(NULL);
		}
		cuddRef(res);
		Cudd_RecursiveDerefZdd(dd, prevZdd);
	    }
	    cuddDeref(res);
	}
	return(res);
    }	/* end of cache look-up */

    if (Cudd_IsComplement(B)) {
	Bt = Cudd_Not(cuddT(Breg));
	Be = Cudd_Not(cuddE(Breg));
    } else {
	Bt = cuddT(Breg);
	Be = cuddE(Breg);
    }

    id = (int) Breg->index;
    level = cuddI(dd,id);
    t = zddPortFromBddStep(dd, Bt, level+1);
    if (t == NULL) return(NULL);
    cuddRef(t);
    e = zddPortFromBddStep(dd, Be, level+1);
    if (e == NULL) {
	Cudd_RecursiveDerefZdd(dd, t);
	return(NULL);
    }
    cuddRef(e);
    res = cuddZddGetNode(dd, id, t, e);
    if (res == NULL) {
	Cudd_RecursiveDerefZdd(dd, t);
	Cudd_RecursiveDerefZdd(dd, e);
	return(NULL);
    }
    cuddRef(res);
    Cudd_RecursiveDerefZdd(dd, t);
    Cudd_RecursiveDerefZdd(dd, e);

    cuddCacheInsert1(dd,Cudd_zddPortFromBdd,B,res);

    for (level--; level >= expected; level--) {
	prevZdd = res;
	id = dd->invperm[level];
	res = cuddZddGetNode(dd, id, prevZdd, prevZdd);
	if (res == NULL) {
	    Cudd_RecursiveDerefZdd(dd, prevZdd);
	    return(NULL);
	}
	cuddRef(res);
	Cudd_RecursiveDerefZdd(dd, prevZdd);
    }

    cuddDeref(res);
    return(res);

} /* end of zddPortFromBddStep */


/**
  @brief Performs the recursive step of Cudd_zddPortToBdd.

  @sideeffect None

*/
static DdNode *
zddPortToBddStep(
  DdManager * dd /* manager */,
  DdNode * f /* %ZDD to be converted */,
  int  depth /* recursion depth */)
{
    DdNode *one, *zero, *T, *E, *res, *var;
    int index;
    int level;

    statLine(dd);
    one = DD_ONE(dd);
    zero = DD_ZERO(dd);
    if (f == zero) return(Cudd_Not(one));

    if (depth == dd->sizeZ) return(one);

    index = dd->invpermZ[depth];
    level = cuddIZ(dd,f->index);
    var = cuddUniqueInter(dd,index,one,Cudd_Not(one));
    if (var == NULL) return(NULL);
    cuddRef(var);

    if (level > depth) {
	E = zddPortToBddStep(dd,f,depth+1);
	if (E == NULL) {
	    Cudd_RecursiveDeref(dd,var);
	    return(NULL);
	}
	cuddRef(E);
	res = cuddBddIteRecur(dd,var,Cudd_Not(one),E);
	if (res == NULL) {
	    Cudd_RecursiveDeref(dd,var);
	    Cudd_RecursiveDeref(dd,E);
	    return(NULL);
	}
	cuddRef(res);
	Cudd_RecursiveDeref(dd,var);
	Cudd_RecursiveDeref(dd,E);
	cuddDeref(res);
	return(res);
    }

    res = cuddCacheLookup1(dd,Cudd_zddPortToBdd,f);
    if (res != NULL) {
	Cudd_RecursiveDeref(dd,var);
	return(res);
    }

    T = zddPortToBddStep(dd,cuddT(f),depth+1);
    if (T == NULL) {
	Cudd_RecursiveDeref(dd,var);
	return(NULL);
    }
    cuddRef(T);
    E = zddPortToBddStep(dd,cuddE(f),depth+1);
    if (E == NULL) {
	Cudd_RecursiveDeref(dd,var);
	Cudd_RecursiveDeref(dd,T);
	return(NULL);
    }
    cuddRef(E);

    res = cuddBddIteRecur(dd,var,T,E);
    if (res == NULL) {
	Cudd_RecursiveDeref(dd,var);
	Cudd_RecursiveDeref(dd,T);
	Cudd_RecursiveDeref(dd,E);
	return(NULL);
    }
    cuddRef(res);
    Cudd_RecursiveDeref(dd,var);
    Cudd_RecursiveDeref(dd,T);
    Cudd_RecursiveDeref(dd,E);
    cuddDeref(res);

    cuddCacheInsert1(dd,Cudd_zddPortToBdd,f,res);

    return(res);

} /* end of zddPortToBddStep */


ACTIVATE 0  ; Activate row buffer
STORE 1  ; Store to row 1
STORE 2  ; Store to row 2
STORE 3  ; Store to row 3
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %21, %22,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %26, %27,
STORE 4  ; Store to row 4
BRANCH label %23, !6
STORE 5  ; Store to row 5
BRANCH label %18, !8
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %46, %47,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %51, %52,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %56, %57,
STORE 6  ; Store to row 6
STORE 7  ; Store to row 7
BRANCH label %53, !9
STORE 8  ; Store to row 8
BRANCH label %48, !10
STORE 9  ; Store to row 9
BRANCH label %43, !11
STORE 10  ; Store to row 10
STORE 11  ; Store to row 11
STORE 12  ; Store to row 12
STORE 13  ; Store to row 13
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %34, %35,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %61, %62,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %66, %67,
STORE 14  ; Store to row 14
BRANCH label %63, !12
STORE 15  ; Store to row 15
STORE 16  ; Store to row 16
STORE 17  ; Store to row 17
STORE 18  ; Store to row 18
STORE 19  ; Store to row 19
STORE 20  ; Store to row 20
STORE 21  ; Store to row 21
STORE 22  ; Store to row 22
BRANCH label %58, !13
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %120, %121,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %125, %126,
STORE 23  ; Store to row 23
BRANCH label %122, !14
STORE 24  ; Store to row 24
BRANCH label %117, !15
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %151, %152,
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %156, %157,
STORE 25  ; Store to row 25
BRANCH label %153, !16
STORE 26  ; Store to row 26
BRANCH label %148, !17
STORE 27  ; Store to row 27
STORE 28  ; Store to row 28
STORE 29  ; Store to row 29
STORE 30  ; Store to row 30
STORE 31  ; Store to row 31
STORE 32  ; Store to row 32
STORE 33  ; Store to row 33
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %9, %10,
STORE 34  ; Store to row 34
STORE 35  ; Store to row 35
STORE 36  ; Store to row 36
STORE 37  ; Store to row 37
STORE 38  ; Store to row 38
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %10, %11,
STORE 39  ; Store to row 39
STORE 40  ; Store to row 40
BRANCH i1 %7, %8,
STORE 41  ; Store to row 41
STORE 42  ; Store to row 42
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %10, %11,
BRANCH i1 %13, %14,
STORE 43  ; Store to row 43
STORE 44  ; Store to row 44
STORE 45  ; Store to row 45
BRANCH i1 %7, %8,
STORE 46  ; Store to row 46
STORE 47  ; Store to row 47
BRANCH i1 %10, %11,
STORE 48  ; Store to row 48
STORE 49  ; Store to row 49
BRANCH i1 %13, %14,
STORE 50  ; Store to row 50
BRANCH label %10, !18
STORE 51  ; Store to row 51
BRANCH i1 %9, %10,
STORE 52  ; Store to row 52
STORE 53  ; Store to row 53
STORE 54  ; Store to row 54
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %9, %10,
STORE 55  ; Store to row 55
STORE 56  ; Store to row 56
STORE 57  ; Store to row 57
STORE 58  ; Store to row 58
STORE 59  ; Store to row 59
STORE 60  ; Store to row 60
STORE 61  ; Store to row 61
BRANCH i1 %7, %8,
STORE 62  ; Store to row 62
STORE 63  ; Store to row 63
LUT_PROG_CMP 0xF, 0xC0  ; Program comparison LUTs
COMPARE  ; Execute comparison
BRANCH i1 %10, %11,
BRANCH i1 %13, %14,
STORE 64  ; Store to row 64
STORE 65  ; Store to row 65
STORE 66  ; Store to row 66
STORE 67  ; Store to row 67
BRANCH i1 %13, %14,
STORE 68  ; Store to row 68
BRANCH label %11, !19
STORE 69  ; Store to row 69
STORE 70  ; Store to row 70
STORE 71  ; Store to row 71
STORE 72  ; Store to row 72
STORE 73  ; Store to row 73
BRANCH i1 %15, %16,
BRANCH i1 %8, %9,
BRANCH label %5, !20
STORE 74  ; Store to row 74
BRANCH i1 %9, %10,
STORE 75  ; Store to row 75
STORE 76  ; Store to row 76
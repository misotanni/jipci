# jipci
The repository for *jipci*, the Just Intonation Pansophical Conversion Instrument.

## General

*jipci* is a universal just intonation converter; its purpose is to convert data about just intonation intervals between different methods of representation.

The converter takes a command that consists of three parts, e.g.
`fjs ratio 45/32`

The parts are always separated by spaces, and spaces are found exactly nowhere else.

- Part 1: target (output) system
- Part 2: input system
- Part 3: input data

The converter will interpret the input data according to the input system, and will convert this data to a new format according to the target system, which it will then output. `fjs ratio 45/32` is therefore understood as follows: 'I want to convert into the **FJS** the following **ratio**: **45/32**'. And since 45/32 is called `A4^5` in the FJS, the output will be `A4^5`.

The converter only handles just intonation intervals. It does not handle individual notes.

# Supported systems

The following systems are supported in both output and input:

- Ratios: `ratio`
- Monzos (interval vectors): `monzo`
- The Functional Just System: `fjs`
- Color notation: `color`
- Helmholtz-Ellis notation: `he`
- Ben Johnston's notation: `bj`

Helmholtz-Ellis is restricted to the 61-limit, therefore any higher-limit interval in the input will raise an error if attempting to convert it into Helmholtz-Ellis. Ben Johnston is restricted to the 31-limit, therefore any higher-limit interval in the input will raise an error if attempting to convert it into Ben Johnston. There are no restrictions in the remaining systems.

The first two are collectively referred to as 'pure' systems, as they reflect the numerical content of the intervals in the simplest form. The latter four, designed for use in musical composition and analysis, are collectively considered to be EJI (Extended Just Intonation) systems. This includes the two 'good' systems (the FJS and color notation), as well as the two 'bad' systems popular in academia (Helmholtz-Ellis and Ben Johnston).

The following systems are supported in output only:

- Size in cents: `cents`
- Size in millioctaves: `mo`

Both will be given to 4 decimal places.

## Format

### Ratios

Ratios always consist of two positive integers separated by one slash. Ratios are allowed to be not in simplest form, but this will never happen in the output.

These are well-formed ratios: `5/4`, `729/640`, `1/1`, `531441/524288`, `5/6`.

These are not: `5`, `2/`, `5//1`, `/3`, `-5/4`, `5/-4`, `4/5/6`, `5:4`, `10:12:15`, `0/3`, `7/0`, `0/0`.

These are well-formed ratios, but will never be seen in the output: `9/6`, `49/7`.

### Monzos

Monzos always consist of integers separated by the `,` symbol and surrounded by square brackets. There are no spaces inside a monzo. A monzo can also consist of a pair of empty square brackets. Monzos are allowed to have zero as their last coefficient in the input, but this will never happen in the output.

These are well-formed monzos: `[2]`, `[5,1]`, `[0,0,1]`, `[1,1,-1]`, `[2,0,-3,1]`, `[5,1,0,0,0,0,0,0,-1]`, `[]`.

These are not: `[3 ]`, `[2, -1]`, `[1,1,-]`, `[ ]`, `[1.5,2,-1]`, `[,,3]`.

These are well-formed monzos, but will never be seen in the output: `[0]`, `[1,1,-1,0,0,0]`.

### Intervals (general for EJI systems)

Intervals consist of an octave prefix, followed by a variant, followed by the stepspan, followed by any extended just intonation accidentals specific to the EJI system in question. Here, everything aside from these just intonation accidentals is described.

The variant and stepspan notation is widely known: `P5` means a perfect fifth, `M3` means a major third, etc. Doubly, triply, etc. augmented or diminished intervals repeat the `A` or `d`: `AA4` is a doubly augmented fourth. Color notation use alternative variants; these will be discussed in the color notation section.

The octave prefix consists of an optional minus sign followed by a string of `c` letters to represent octave shifts. This has been used in Kite's color notation, but the version used in the converter is slightly different: negative octave shifts are allowed, thus `-c` is one octave down, `-cc` is two octaves down, etc. The default octave includes `P1` and excludes `P8`. For example, `cM2` = `M9`, `ccM2` = `cM9` = `M16`, `-cM2` = 'negative m7'. The converter does NOT use negative intervals (e.g. 'negative P4' = 3/4); instead, it uses negative octave shifts, so 3/4 = `-cP5`.

Any equivalent form (except negative intervals, which are not used) of octave notation will be correctly interpreted (e.g. `M16`, `cM9` and `ccM2` will all be interpreted the same way in the input), but only the 'smart' form will be seen in the output. The 'smart' form is usually the form in the default octave, however, `P8` is used instead of `cP1`, and `-cd8` is used instead of `d1` (and the like). This does not apply to color notation. In color notation, a different algorithm is used to determine which form is 'smart' and thus outputted, since color notation does make use of diminished unisons.

These are well-formed intervals: `P4`, `P1`, `cm3`, `cA1`, `ccM3`, `-ccM7`, `ddd5`, `AA4`, `-cAAAAAAA3`, `P8`.

These are not: `M4`, `P3`, `m-2`, `-m2`, `A0`, `MP3`, `AM6`, `--cd4`.

These are well-formed intervals, but will never be seen in the output: `A8`, `cP1`, `d1`, `M10`, `P49`.

### Helmholtz-Ellis notation

Because Helmholtz-Ellis requires a special font to represent its notation, it has been ASCIIfied for the purpose of this converter.

For the 31-limit, every Helmholtz-Ellis accidental has been replaced by its prime number with a plus sign (upward) or a minus sign (downward). The 5-limit accidentals, which are combinations of standard accidentals with arrows, have been 'split' for this purpose, with the arrow now being considered independent. Therefore `+7` is the upward 7-arrow, `+31` is the plus, `-31` is the minus, `+29` is the triple slash, `-29` is the triple backslash, etc.

For the 61-limit, accidentals are reused with curly brackets around them, so this has been reflected in the ASCIIfication. For example, `+{17}` is the upward accidental for 37, since it is based on the upward accidental for 17, but with curly brackets around it. A special case is the accidental for 47, which is ASCIIfied as `{49}`, as it is based on a double accidental for 7.

These accidentals can appear in any order, but in the output they will always appear sorted in non-descending order by size of the prime they stand for. Also, it is legal to include both an accidental and its inverse, but this will never happen in the output.

These are well-formed Helmholtz-Ellis intervals: `M3-5`, `cm3-7`, `m2+5-17`, `P8-11-31`, `ccM2+11+31-{17}`.

These are not: `M3+9`, `M2+11+37`, `ccP1+257`, `m3-{11}`.

These are well-formed Helmholtz-Ellis intervals, but will never be seen in the output: `M2-7-5`, `P8-31-11`, `P5+5-5`.

### Ben Johnston's notation

All the accidentals except for the syntonic comma are handled in the following way. Every accidental has been given an ASCII form:

- 35/36 and 36/35 become `7` and `L`;
- 33/32 and 32/33 become `^` and `v`;
- All higher accidentals take the prime number itself for the otonal accidental, or with a minus sign for the utonal accidental; e.g. 95/96 and 96/95 become `19` and `-19`.

These accidentals are separated by the `,` symbol. They can appear in any order, but in the output they will always appear sorted in non-descending order by size of the prime they stand for. Also, it is legal to include both an accidental and its inverse, but this will never happen in the output.

After this, syntonic commas are handled, differently in the output than in the input.

In the **output**, a clause which describes syntonic commas appears. It is enclosed in parentheses and will list all the pitch classes (from among C, D, E, F, G, A, B) where syntonic comma adjustments are needed to reach the target interval, and will then show the sequence of these adjustments. The clause will not show those notes which require no adjustment. The note and adjustment sequences will be separated from each other by the `,` symbol. If no pitch class requires an adjustment, the clause will be empty, in which case it will just be a pair of parentheses.

Example: The input `5/4` becomes `M3(D+)`. This means that in order to build a 5/4 from any D (including sharps/flats, e.g. Db or D#), it is required to build a major third and add a plus, so e.g. Db becomes F+, and D becomes F#+, but in order to build a 5/4 from any other note, e.g. C or F# or Ab, simply a major third is required, so C becomes E, F# becomes A#, and Ab becomes C.

A more complex example would be `M2(D+,E+,G+,B+)`, the output of `9/8`. This means that in order to build a 9/8 from any D, any E, any G, or any B (including any sharps/flats), one must build a major second and add a plus, while on any C, any F, or any A (including any sharps/flats), one must build simply a major second.

In the **input**, things are handled differently. It is only required to choose **one** pitch class and specify the syntonic comma adjustment for that pitch class (even if that adjustment for that pitch class is zero), and the converter can work out the interval from that information only. In fact, it is **not** allowed to give information about more than one, because such superfluous data could be mutually contradictory. For example, to get `9/8`, `M2(D+)` is a valid input, and so is `M2(E+)`, and `M2(C)`, but **not** `M2(D+,E+,G+,B+)` or `M2(C,D+)` or `M2(G+,B+)`. Therefore, in the input, one must describe the size of the interval, and then describe what the syntonic comma adjustment would be for **one** pitch class, which can be chosen freely. It is allowed for the note in the input to be modified by both pluses and minuses, even though this is redundant. It is also allowed for the note in the input to be lowercase instead of uppercase, even though all notes will be uppercase in the output.

These are well-formed Ben Johnston outputs: `ccM3(D+)`, `P4,L(F-,A-)`, `P1,17()`, `A1,v,v()`, `P5,L,^(C-,E-,F-,G-,A-)`.

These are not: `P1`, `M3(d+)`, `P4,L(F-)`, `M2,37()`, `P1,11()`, `P5,^,L(C-,E-,F-,G-,A-)`.

These are well-formed Ben Johnston inputs: `ccM3(D+)`, `P4,L(f-)`, `P1,17(C)`, `A1,v,v(F++)`, `P5,L,^(c-)`, `P5,^,L(C-)`, `P5(G+--+)`.

These are not: `P1`, `P1()`, `P4,L(F-,A-)`, `M2(d+,e+,g+,b+)`.

### FJS

Uses the same ASCIIfication as specified by the FJS docs.

In the output, no adjustments are ever multiplied, and all adjustments are listed in non-descending order of the associated prime. In the input, `1` is allowed as an adjustment, and it is legal to include both an adjustment and its inverse, even though it has no effect. Also `3` is allowed as a Pythagorean comma adjustment, although it will never appear in the output.

These are well-formed FJS intervals: `M3^5`, `cm3^7`, `M2^5,7`, `d5^7_5`, `A7^5,5,5`, `P1^65537`.

These are not: `d5_5^7`, `A1_2`, `P1^0`, `m6^-5`, `M3_`, `P8^_5`.

These are well-formed FJS intervals, but will never be seen in the output: `m2^3,5_7`, `m2^15_7`, `cP5^1,1,1_1,1`, `P5^5_5`, `M2^7,5`, `A7^25,5`, `A7^125`.

### Color notation

The ASCIIfication for color notation is mostly the same as the original, but with a few changes.

As mentioned before, negative intervals are not used; instead, negative octave shifts are used, by prefixing the string of `c` letters with a minus sign. Similarly, superscripts for n-tuple colors are not used; instead, the color is always repeated, so e.g. the trigu second is `ggg2`. In the input, it is legal to include both `y` and `g`, or both `1o` and `1u`, etc. even though it has no effect. Also, `p` and `q` are allowed as Pythagorean comma adjustments, although they will never appear in the output.

These are well-formed color notation intervals: `y3`, `sw6`, `zg5`, `cc1o4`, `ggg2`, `65537o1`.

These are not: `j3`, `3g2`, `cc11o4`, `5o7`.

These are well-formed color notation intervals, but will never be seen in the output: `LLzq2`, `gz5`, `Lsw1`, `cyg5`.

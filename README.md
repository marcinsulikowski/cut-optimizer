# Cut Optimizer

The program finds the optimal order of cutting polylines on a 2D plane. It
minimizes moves of the cutting head along the X axis.

## Usage

    ./optimize [input_file]

If no input file is given, the input is read form the standard input stream.
Output is always written to the standard output stream.

## Input

The input is given as a series of lines in one of the following forms:

* For open polylines, we specify their first and last point:

      <poly-name> O <start-x> <start-y> <end-x> <end-y>

* For closed polylines, we specify their bounding box:

      <poly-name> C <x-min> <y-min> <x-max> <y-max>

`<poly-name>` can be any string with no spaces. It is used to identify the
polyline in the output. All `x` and `y` coordinates must be non-negative
integers.

## Output

The output is a series of lines in the following form:

    <poly-name> <direction> (<start-x>, <start-y>) -> (<end-x>, <end-y>)

which specify in which order and direction to cut.

* `<poly-name>` is a name of the polyline
* `<direction>` is one of: `forward` (cut an open polyline from its start to
  its end), `<reverse>` (cut an open polyline from its end to its start), or
  `closed` (cut a closed polyline from the given starting point back to the
  same point).


module alu_top(
    input  [31:0] a,
    input  [31:0] b,
    input  [2:0] op,

    input  [1:0] expected_residue,
    input        expected_parity,

    output [31:0] result,
    output        fault_flag
);

wire residue_fail;
wire parity_fail;

alu_core u_alu (
    .a(a),
    .b(b),
    .op(op),
    .result(result)
);

checker u_checker (
    .result(result),
    .expected_residue(expected_residue),
    .expected_parity(expected_parity),
    .residue_fail(residue_fail),
    .parity_fail(parity_fail),
    .fault_flag(fault_flag)
);

endmodule

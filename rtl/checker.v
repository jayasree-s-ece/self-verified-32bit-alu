module checker(
    input [31:0] result,
    input [1:0] expected_residue,
    input expected_parity,

    output residue_fail,
    output parity_fail,
    output fault_flag
);

wire [1:0] actual_residue;
assign actual_residue = result % 3;

wire actual_parity;
assign actual_parity = ^result;

assign residue_fail = (actual_residue != expected_residue);
assign parity_fail  = (actual_parity  != expected_parity);

assign fault_flag = residue_fail | parity_fail;

endmodule

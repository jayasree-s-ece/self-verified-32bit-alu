module tb_fault_inject;

reg  [31:0] a;
reg  [31:0] b;
reg  [2:0]  op;

reg  [1:0] expected_residue;
reg        expected_parity;

wire [31:0] result;
wire fault_flag;

alu_top dut (
    .a(a),
    .b(b),
    .op(op),
    .expected_residue(expected_residue),
    .expected_parity(expected_parity),
    .result(result),
    .fault_flag(fault_flag)
);

initial begin

    // ADD test
    a = 32'd10;
    b = 32'd5;
    op = 3'b000;

    // Correct result = 15
    expected_residue = 0;
    expected_parity  = 1'b0;

    #10;

    $display("Result = %d", result);
    $display("Fault Flag = %b", fault_flag);

    $finish;
end

endmodule

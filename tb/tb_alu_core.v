module tb_alu_core;

reg [31:0] a, b;
reg [2:0] op;
wire [31:0] result;

alu_core dut (
    .a(a),
    .b(b),
    .op(op),
    .result(result)
);

initial begin
    // ADD
    a = 10; b = 5; op = 3'b000;
    #10;
    $display("ADD: %d", result);

    // SUB
    a = 10; b = 5; op = 3'b001;
    #10;
    $display("SUB: %d", result);

    // AND
    a = 12; b = 10; op = 3'b010;
    #10;
    $display("AND: %d", result);

    $finish;
end

endmodule

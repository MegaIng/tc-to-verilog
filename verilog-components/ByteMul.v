module TC_ByteMul (a, b, out);
    input [7:0] a;
    input [7:0] b;
    output [15:0] out;

    assign out = a * b;
endmodule


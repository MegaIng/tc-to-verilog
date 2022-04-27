module TC_Add8 (a, b, ci, out, co);
    input [7:0] a;
    input [7:0] b;
    input ci;
    output [7:0] out;
    output co;

    assign {co, out} = a + b + ci;
endmodule


module TC_Neg8 (in, out);
    input [7:0] in;
    output [7:0] out;

    assign out = 8'b0000_0000 - in;
endmodule


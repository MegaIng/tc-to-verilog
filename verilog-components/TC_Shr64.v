module TC_Shr64 (in, shift, out);
    input [63:0] in;
    input [5:0] shift;
    output [63:0] out;

    assign out = in >> shift;
endmodule


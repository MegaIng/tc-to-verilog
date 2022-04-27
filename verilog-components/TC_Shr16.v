module TC_Shr16 (in, shift, out);
    input [15:0] in;
    input [3:0] shift;
    output [15:0] out;

    assign out = in >> shift;
endmodule


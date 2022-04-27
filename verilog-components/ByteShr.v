module TC_ByteShr (in, shift, out);
    input [7:0] in;
    input [2:0] shift;
    output [7:0] out;

    assign out = in >> shift;
endmodule


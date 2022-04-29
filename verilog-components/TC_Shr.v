module TC_Shr (in, shift, out);
    parameter BIT_WIDTH = 1;
    input [BIT_WIDTH-1:0] in;
    input [7:0] shift;
    output [BIT_WIDTH-1:0] out;

    assign out = in >> shift;
endmodule


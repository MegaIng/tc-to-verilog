module TC_Neg (in, out);
    parameter size = 1;
    input [size-1:0] in;
    output [size-1:0] out;

    assign out = {size{1'b0}} - in;
endmodule


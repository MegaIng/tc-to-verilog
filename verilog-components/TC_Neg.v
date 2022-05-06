module TC_Neg (in, out);
    parameter UUID = 0;
    parameter NAME = "";
    parameter BIT_WIDTH = 1;
    input [BIT_WIDTH-1:0] in;
    output [BIT_WIDTH-1:0] out;

    assign out = {BIT_WIDTH{1'b0}} - in;
endmodule


module TC_And3(in0, in1, in2, out);
    parameter BIT_WIDTH = 1;
    input [BIT_WIDTH-1:0] in0;
    input [BIT_WIDTH-1:0] in1;
    input [BIT_WIDTH-1:0] in2;
    output [BIT_WIDTH-1:0] out;
    
    assign out = in0 & in1 & in2;
endmodule


module TC_Maker64 (in0, in1, in2, in3, in4, in5, in6, in7, out);
    input [7:0] in0;
    input [7:0] in1;
    input [7:0] in2;
    input [7:0] in3;
    input [7:0] in4;
    input [7:0] in5;
    input [7:0] in6;
    input [7:0] in7;
    output [63:0] out;
    
    assign out = {in7, in6, in5, in4, in3, in2, in1, in0};
endmodule


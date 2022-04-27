module TC_Maker32 (in0, in1, in2, in3, out);
    input [7:0] in0;
    input [7:0] in1;
    input [7:0] in2;
    input [7:0] in3;
    output [31:0] out;
    
    assign out = {in3, in2, in1, in0};
endmodule


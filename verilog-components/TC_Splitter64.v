module TC_Splitter64 (in, out0, out1, out2, out3, out4, out5, out6, out7);
    input [63:0] in;
    output [7:0] out0;
    output [7:0] out1;
    output [7:0] out2;
    output [7:0] out3;
    output [7:0] out4;
    output [7:0] out5;
    output [7:0] out6;
    output [7:0] out7;
    
    assign {out7, out6, out5, out4, out3, out2, out1, out0} = in;
endmodule


module TC_Nand(in0, in1, out);
    parameter size = 1;
    input [size-1:0] in0;
    input [size-1:0] in1;
    output [size-1:0] out;
    
    assign out = ~(in0 & in1);
endmodule


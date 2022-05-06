module TC_Stack (clk, rst, pop, push, in, out);
    parameter UUID = 0;
    parameter NAME = "";
    input clk;
    input rst;
    input pop;
    input push;
    input [7:0] in;
    output [7:0] out;
    
    reg [7:0] mem [0:255];
    reg [7:0] sp;

    integer i;
    
    initial begin
        for (i=0; i<256; i=i+1) mem[i] <= 8'b0000_0000;
        sp <= 8'b0000_0000;
        out <= 8'b0000_0000;
    end
    
    always @ (posedge pop) begin
        if (rst) begin
            out <= 8'b0000_0000;
        end else begin
            sp <= sp - 1;
            out <= mem[sp];
        end
    end
    always @ (negedge clk) begin
        if (rst) begin
            sp <= 8'b0000_0000;
            for (i=0; i<256; i=i+1) mem[i] <= 8'b0000_0000;
        end else if (push) begin
            mem[sp] <= in;
            sp <= sp + 1;
        end
    end
endmodule


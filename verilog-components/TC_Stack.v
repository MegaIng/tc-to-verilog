module TC_Stack (clk, rst, pop, push, in, out);
    input clk;
    input rst;
    input pop;
    input push;
    input [7:0] in;
    output [7:0] out;
    
    reg [7:0] mem [0:255];
    reg [7:0] sp;
    reg [7:0] outval;

    integer i;
    
    always @ (posedge clk or rst) begin
        if (rst) begin
            sp = {8{1'b0}};
            for (i=0; i<256; i=i+1) begin
                mem[i] = {8{1'b0}};
            end
            outval = 8'bZZZZ_ZZZZ;
        end else if (pop) begin
            sp <= sp - 1;
            outval <= mem[sp];
        end else begin
            outval = 8'bZZZZ_ZZZZ;
        end
    end
    
    always @ (negedge clk) begin
        if (push && !rst) begin
            mem[sp] <= in;
            sp <= sp + 1;
        end
    end
endmodule


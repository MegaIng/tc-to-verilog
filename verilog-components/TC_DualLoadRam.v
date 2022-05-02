module TC_DualLoadRam (clk, rst, load0, save, address0, in, load1, address1, out0, out1);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 256;
    input clk;
    input rst;
    input load0;
    input save;
    input [15:0] address0;
    input [BIT_WIDTH-1:0] in;
    input load1;
    input [15:0] address1;
    output [BIT_WIDTH-1:0] out0;
    output [BIT_WIDTH-1:0] out1;

    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];

    initial begin
        for (i=0; i<MEM_WORDS; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        out0 <= {64{1'b0}};
        out1 <= {64{1'b0}};
    end

    always @ (address0 or rst) begin
        if (load0 && !rst)
            out0 <= mem[address0];
        else
            out0 <= {BIT_WIDTH{1'b0}};
    end
    always @ (address1 or rst) begin
        if (load1 && !rst)
            out1 <= mem[address1];
        else
            out1 <= {BIT_WIDTH{1'B0}};
    end
    always @ (negedge clk) begin
        if (rst)
            for (i=0; i<MEM_WORDS; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        else if (save)
            mem[address0] <= in;
    end
endmodule

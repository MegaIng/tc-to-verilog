module TC_FastRam (clk, rst, load, save, address, in0, in1, in2, in3, out0, out1, out2, out3);
    parameter BIT_WIDTH = 16;
    parameter BIT_DEPTH = 256;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [63:0] in0;
    input [63:0] in1;
    input [63:0] in2;
    input [63:0] in3;
    output reg [63:0] out0;
    output reg [63:0] out1;
    output reg [63:0] out2;
    output reg [63:0] out3;
    
    reg [BIT_WIDTH-1:0] mem [0:BIT_DEPTH];
    
    integer i;
    
    initial begin
        for (i=0; i<BIT_DEPTH; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        out0 <= {64{1'b0}};
        out1 <= {64{1'b0}};
        out2 <= {64{1'b0}};
        out3 <= {64{1'b0}};
    end
    
    always @ (address or rst) begin
        if (load && !rst) begin
            if (BIT_WIDTH < 64)
                out0 <= {{(64-BIT_WIDTH){1'b0}}, mem[address][BIT_WIDTH-1:0]};
            else
                out0 <= mem[address][63:0];
            if (BIT_WIDTH >= 128)
                out1 <= mem[address][127:64];
            else
                out1 <= {64{1'b0}};
            if (BIT_WIDTH == 256) begin
                out2 <= mem[address][191:128];
                out3 <= mem[address][255:192];
            end else begin
                out2 <= {64{1'b0}};
                out3 <= {64{1'b0}};
            end
        end else begin
            out0 <= {BIT_WIDTH{1'b0}};
            out1 <= {BIT_WIDTH{1'b0}};
            out2 <= {BIT_WIDTH{1'b0}};
            out3 <= {BIT_WIDTH{1'b0}};
        end
    end
    always @ (negedge clk) begin
        if (rst)
            for (i=0; i<BIT_DEPTH; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        else if (save) begin
            if (BIT_WIDTH < 64)
                mem[address] <= in0[BIT_WIDTH-1:0];
            else
                mem[address][63:0] <= in0;
            if (BIT_WIDTH >= 128)
                mem[address][127:64] <= in1;
            if (BIT_WIDTH == 256) begin
                mem[address][191:128] <= in2;
                mem[address][255:192] <= in3;
            end
        end
    end
endmodule

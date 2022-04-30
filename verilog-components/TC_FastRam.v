module TC_FastRam (clk, rst, load, save, address, in0, in1, in2, in3, out0, out1, out2, out3);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 65536;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in0;
    input [BIT_WIDTH-1:0] in1;
    input [BIT_WIDTH-1:0] in2;
    input [BIT_WIDTH-1:0] in3;
    output [BIT_WIDTH-1:0] out0;
    output [BIT_WIDTH-1:0] out1;
    output [BIT_WIDTH-1:0] out2;
    output [BIT_WIDTH-1:0] out3;
    reg [BIT_WIDTH-1:0] outval0;
    reg [BIT_WIDTH-1:0] outval1;
    reg [BIT_WIDTH-1:0] outval2;
    reg [BIT_WIDTH-1:0] outval3;
    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];
    always @ (posedge clk or rst) begin
        if (load && !rst) begin
            outval0 <= mem[address];
            outval1 <= mem[address+1];
            outval2 <= mem[address+2];
            outval3 <= mem[address+3];
        end else begin
            outval0 <= {BIT_WIDTH{1'bZ}};
            outval1 <= {BIT_WIDTH{1'bZ}};
            outval2 <= {BIT_WIDTH{1'bZ}};
            outval3 <= {BIT_WIDTH{1'bZ}};
        end
    end
    always @ (negedge clk) begin
        if (save) begin
            mem[address] <= in0;
            mem[address+1] <= in1;
            mem[address+2] <= in2;
            mem[address+3] <= in3;
        end
    end
    assign out0 = outval0;
    assign out1 = outval1;
    assign out2 = outval2;
    assign out3 = outval3;
endmodule

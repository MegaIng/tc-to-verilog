module TC_CheapRamLat (clk, rst, load, save, address, in0, in1, in2, in3, ready, out0, out1, out2, out3);
    parameter BIT_WIDTH = 16;
    parameter BIT_DEPTH = 256;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in0;
    input [BIT_WIDTH-1:0] in1;
    input [BIT_WIDTH-1:0] in2;
    input [BIT_WIDTH-1:0] in3;
    output reg ready;
    output reg [BIT_WIDTH-1:0] out0;
    output reg [BIT_WIDTH-1:0] out1;
    output reg [BIT_WIDTH-1:0] out2;
    output reg [BIT_WIDTH-1:0] out3;

    reg readywait;
    reg [BIT_WIDTH-1:0] outwait0;
    reg [BIT_WIDTH-1:0] outwait1;
    reg [BIT_WIDTH-1:0] outwait2;
    reg [BIT_WIDTH-1:0] outwait3;
    reg [BIT_WIDTH-1:0] mem [0:BIT_DEPTH];

    initial begin
        for (i=0; i<BIT_DEPTH; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        out0 <= {BIT_WIDTH{1'b0}};
        out1 <= {BIT_WIDTH{1'b0}};
        out2 <= {BIT_WIDTH{1'b0}};
        out3 <= {BIT_WIDTH{1'b0}};
    end

    always @ (posedge clk) begin
        if (rst) begin
            out0 <= {BIT_WIDTH{1'b0}};
            out1 <= {BIT_WIDTH{1'b0}};
            out2 <= {BIT_WIDTH{1'b0}};
            out3 <= {BIT_WIDTH{1'b0}};
            ready <= 1'b0;
            outwait0 <= {BIT_WIDTH{1'b0}};
            outwait1 <= {BIT_WIDTH{1'b0}};
            outwait2 <= {BIT_WIDTH{1'b0}};
            outwait3 <= {BIT_WIDTH{1'b0}};
            readywait <= 1'b0;
        end else begin
            out0 <= outwait0;
            out1 <= outwait1;
            out2 <= outwait2;
            out3 <= outwait3;
            ready <= readywait;
            if (load) begin
                outwait0 <= mem[address];
                outwait1 <= mem[address+1];
                outwait2 <= mem[address+2];
                outwait3 <= mem[address+3];
                readywait <= 1'b1;
            end else begin
                outwait0 <= {BIT_WIDTH{1'b0}};
                outwait1 <= {BIT_WIDTH{1'b0}};
                outwait2 <= {BIT_WIDTH{1'b0}};
                outwait3 <= {BIT_WIDTH{1'b0}};
                readywait <= 1'b0;
            end
        end
    end
    always @ (negedge clk) begin
        if (rst)
            for (i=0; i<BIT_DEPTH; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        else if (save) begin
            mem[address] <= in0;
            mem[address+1] <= in1;
            mem[address+2] <= in2;
            mem[address+3] <= in3;
        end
    end
endmodule

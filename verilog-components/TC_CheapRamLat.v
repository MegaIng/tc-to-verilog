module TC_CheapRamLat (clk, rst, load, save, address, in, ready, out);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 65536;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in;
    output tri0 ready;
    output tri0 [BIT_WIDTH-1:0] out;
    reg readywait;
    reg readyval;
    reg [BIT_WIDTH-1:0] outwait;
    reg [BIT_WIDTH-1:0] outval;
    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];
    always @ (posedge clk) begin
        if (load) begin
            outwait <= mem[address];
            readywait <= 1'b1;
        end else begin
            outwait <= {BIT_WIDTH{1'bZ}};
            readywait <= 1'bZ;
        end
        outval <= outwait;
        readyval <= readywait;
    end
    always @ (negedge clk or rst) begin
        if (rst)
            mem[address] <= {BIT_WIDTH{1'b0}};
        else if (save)
            mem[address] <= in;
    end
    assign out = outval;
    assign ready = readyval;
endmodule
